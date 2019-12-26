"""Configuration settings for running the Python auth samples locally.

In a production deployment, this information should be saved in a database or
other secure storage mechanism.
"""

CLIENT_ID = '6bc89158-5ce6-4754-a5a5-25a0952db9e1'
CLIENT_SECRET = 'Dn_xfwNNhf3m8Gbu=rkn7o.XU/z6Pzq]'
REDIRECT_URI = 'https://fourth-vehicle-251408.appspot.com/login/authorized'
AUTHORITY_URL = 'https://login.microsoftonline.com/common'
AUTH_ENDPOINT = '/oauth2/v2.0/authorize'
TOKEN_ENDPOINT = '/oauth2/v2.0/token'
RESOURCE = 'https://graph.microsoft.com/'
API_VERSION = 'v1.0'
SCOPES = ['User.Read', 'User.ReadBasic.All', 'Calendars.Read']
