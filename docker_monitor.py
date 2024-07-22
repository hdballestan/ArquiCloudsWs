import subprocess
import re
import boto3
import time
from connection import sns_client
import environment as E

container_status_cache = {}

def send_sns_notification(message):
    print(E.SNS_ARN_)
    response = sns_client.publish(
        TopicArn=E.SNS_ARN_,
        Message=message,
        Subject='Masw.ai has stopped suddenly!'
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

def monitor_docker_events():
    process = subprocess.Popen(['docker', 'events', '--filter', 'event=die',
                                '--filter', 'event=stop'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
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

if __name__ == '__main__':
    monitor_docker_events()

