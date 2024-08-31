import time
import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from connection import sns_client
import environment as E
import threading

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def send_sns_notification(message):
    response = sns_client.publish(
        TopicArn=E.SNS_ARN_,
        Message=message,
        Subject='Page Status Notification'
    )
    return response

class MonitoringRequest(BaseModel):
    url: str
    time: int  # Time interval in seconds
    status: str  # Desired status to monitor ('on' or 'off')

def monitor_url(url: str, interval: int, status: str):
    while True:
        try:
            response = requests.get(url)
            if status == "on" and response.status_code == 200:
                message = f"The URL {url} is now online (status code 200)."
                send_sns_notification(message)
                break  # Stop monitoring once the site is online

            elif status == "off" and response.status_code != 200:
                message = f"The URL {url} has gone offline (status code {response.status_code})."
                send_sns_notification(message)
                break  # Stop monitoring once the site is offline

        except requests.RequestException as e:
            if status == "off":
                message = f"The URL {url} has gone offline. Error: {str(e)}"
                send_sns_notification(message)
                break  # Stop monitoring once the site is confirmed offline

        time.sleep(interval)

@app.post("/start-monitoring")
async def start_monitoring(request: MonitoringRequest):
    # Start the monitoring in a separate thread
    thread = threading.Thread(target=monitor_url, args=(request.url, request.time, request.status))
    thread.start()
    return {"status": "Monitoring started", "url": request.url, "check_interval": request.time, "desired_status": request.status}

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})




