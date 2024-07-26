import subprocess
import re
import boto3
import time
from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from connection import sns_client
import environment as E

app = FastAPI()
templates = Jinja2Templates(directory="templates")
container_status_cache = {}

def send_sns_notification(message):
    print(E.SNS_ARN_)
    response = sns_client.publish(
        TopicArn=E.SNS_ARN_,
        Message=message,
        Subject='Page Stopped!'
    )
    return response

def parse_docker_event_line(line):
    match = re.match(r'(\S+) (\S+) (\S+) (\S+)(.*)', line)
    if match:
        timestamp, event_type, action, container_id, attributes = match.groups()
        attributes_dict = dict(re.findall(r'(\S+)=(\S+)', attributes))
        container_name = attributes_dict.get('name', 'N/A')
        return container_id, action, container_name
    return None, None, None

class URLCheckRequest(BaseModel):
    url: str

@app.post("/monitor-docker-events")
async def monitor_docker_events():
    process = subprocess.Popen(['docker', 'events', '--filter', 'event=die', '--filter', 'event=stop'],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in iter(process.stdout.readline, b''):
        line = line.decode('utf-8').strip()
        container_id, action, container_name = parse_docker_event_line(line)
        if container_id and action:
            last_notification_time = container_status_cache.get(container_id, 0)
            current_time = time.time()
            if current_time - last_notification_time > 60:    
                message = f"Container {container_name} has {action}. The server has stopped!!"
                send_sns_notification(message)
                container_status_cache[container_id] = current_time
        else:
            print(f"Ignored line: {line}")
    return {"status": "Monitoring docker events"}

@app.post("/check-url-status")
async def check_url_status(request: URLCheckRequest):
    try:
        response = requests.get(request.url)
        if response.status_code == 200:
            return {"url": request.url, "status": "URL is reachable"}
        else:
            message = "The website is down." 
            send_sns_notification(message)
            return {"url": request.url, "status": f"URL returned status code {response.status_code}"}

    except requests.RequestException as e:
        return {"url": request.url, "status": f"Failed to reach URL. Error: {str(e)}"}

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

