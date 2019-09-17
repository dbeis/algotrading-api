from typing import List 
import json 
import requests
import os

default_fallback_url = 'http://yeet.this'
webhooks = {
    'crawler': os.environ.get('DISCORD_CRAWLER_HOOK', default_fallback_url),
    'api': os.environ.get('DISCORD_API_HOOK', default_fallback_url),
    'training': os.environ.get('DISCORD_TRAINING_HOOK', default_fallback_url),
    'ops': os.environ.get('DISCORD_OPS_HOOK', default_fallback_url),
    'test': os.environ.get('DISCORD_TEST_HOOK', default_fallback_url)
}

colors = {
    'green': int('0x2bd600', 0),
    'orange': int('0xff8400', 0),
    'red': int('0xff1e00', 0),
    'purple': int('0xcf21ff', 0),
    'gray': int('0xababab', 0),
}

def notify(channel: str, body):
    try:
        response = requests.post(webhooks[channel], data=body, headers={'Content-Type': 'application/json'})
    except BaseException as e:
        print(str(e)) # i don't really care if this fails. Ignore if dev and no environment vars are set


def embedding(title: str, description: str = None, color: str = colors['gray']):
    payload =  {
        "title": title
    }

    if description is not None:
        payload["description"] = description
    
    if color is not None:
        payload["color"] = color
    
    return payload

def get_json_payload(username: str = 'bot', content: str = None, embeds: List = []):
    payload = {
        "username": username
    }

    if content is not None:
        payload["content"] = content
    
    payload["embeds"] = embeds

    return json.dumps(payload)

def simple_notification(title: str, message: str, username: str = 'bot', color: str = colors['gray']):
    return get_json_payload(username, None, embeds=[embedding(title, message, color)])

# use these
def status_update(message: str, username: str = 'bot'):
    return simple_notification('Status Update', message, username, colors['green'])

def warning_update(message: str, username: str = 'bot'):
    return simple_notification('Warning', message, username, colors['orange'])

def error_update(message: str, username: str = 'bot'):
    return simple_notification('Error', message, username, colors['red'])

def misc_update(message: str, username: str = 'bot'):
    return simple_notification('Be advised', message, username, colors['gray'])

def human_required_update(message: str, username: str = 'bot'):
    return simple_notification('Action Required', message, username, colors['purple'])
