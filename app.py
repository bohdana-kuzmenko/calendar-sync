"""ADAL/Flask sample for Microsoft Graph """
# Copyright (c) Microsoft. All rights reserved. Licensed under the MIT license.
# See LICENSE in the project root for license information.
import json
import os
import urllib.parse
import uuid

import adal
import flask
import requests

import config

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # enable non-HTTPS for testing

app = flask.Flask(__name__, template_folder='static/templates')
app.debug = True
app.secret_key = 'development'

SESSION = requests.Session()


@app.route('/')
def homepage():
    auth_state = str(uuid.uuid4())
    prompt_behavior = 'select_account'
    params = urllib.parse.urlencode({'response_type': 'code',
                                     'client_id': config.CLIENT_ID,
                                     'redirect_uri': config.REDIRECT_URI,
                                     'state': auth_state,
                                     'resource': config.RESOURCE,
                                     'prompt': prompt_behavior})

    return flask.redirect(config.AUTHORITY_URL + '/oauth2/authorize?' + params)


@app.route('/login/authorized')
def authorized():
    """Handler for the application's Redirect Uri."""
    code = flask.request.args['code']
    auth_context = adal.AuthenticationContext(config.AUTHORITY_URL, api_version=None)
    token_response = auth_context.acquire_token_with_authorization_code(
        code, config.REDIRECT_URI, config.RESOURCE, config.CLIENT_ID, config.CLIENT_SECRET)
    SESSION.headers.update({'Authorization': f"Bearer {token_response['accessToken']}",
                            'User-Agent': 'adal-sample',
                            'Accept': 'application/json',
                            'Content-Type': 'application/json',
                            'SdkVersion': 'sample-python-adal',
                            'return-client-request-id': 'true'})
    return flask.redirect('/graphcall')


@app.route('/graphcall')
def graphcall():
    """Confirm user authentication by calling Graph and displaying some data."""
    endpoint = config.RESOURCE + config.API_VERSION + '/me/calendar/events'
    http_headers = {'client-request-id': str(uuid.uuid4())}
    graphdata = SESSION.get(endpoint, headers=http_headers, stream=False).json()
    events = [ i for i in graphdata.get('value')]
    print(json.dumps(events))
    return json.dumps(events)


@app.route('/test')
def test():
    return 'Hello'


if __name__ == '__main__':
    app.run()
