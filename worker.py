import uuid
import json

import requests

from config import RESOURCE, API_VERSION


def get_calendar(auth_token):
    http_headers = {
        'client-request-id': str(uuid.uuid4()),
        'Authorization': f"Bearer {auth_token}",
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'return-client-request-id': 'true',
    }
    event_keys = [
        'id', 'createdDateTime', 'lastModifiedDateTime',
        'isReminderOn', 'reminderMinutesBeforeStart', 'responseStatus',
        'subject', 'webLink', 'bodyPreview', 'start', 'end', 'location',
        'attenders', 'organizer',
    ]
    endpoint = ''.join([RESOURCE, API_VERSION, '/me/calendar/events?top=10'])
    graph_data = requests.get(
        endpoint, headers=http_headers, stream=False).json()
    return json.dumps(
        [{k: v for k, v in event.items() if k in event_keys} for event in
         graph_data.get('value')])
