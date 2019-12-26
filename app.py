import urllib.parse
import uuid

import adal
from flask import request, redirect, Flask

from config import *
from worker import get_calendar

app = Flask(__name__)
app.debug = True


@app.route('/')
def homepage():
    auth_state = str(uuid.uuid4())
    prompt_behavior = 'select_account'
    params = urllib.parse.urlencode({
        'response_type': 'code',
        'resource': RESOURCE,
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'state': auth_state,
        'prompt': prompt_behavior,
        'admin_consent': True
    })
    redirect_url = ''.join([AUTHORITY_URL, '/oauth2/authorize?', params])
    return redirect(redirect_url)


@app.route('/login/authorized')
def authorized():
    code = request.args['code']
    auth_context = adal.AuthenticationContext(AUTHORITY_URL, api_version=None)
    token_response = auth_context.acquire_token_with_authorization_code(
        code, REDIRECT_URI, RESOURCE, CLIENT_ID, CLIENT_SECRET)
    return get_calendar(token_response['accessToken'])


if __name__ == '__main__':
    app.run()
