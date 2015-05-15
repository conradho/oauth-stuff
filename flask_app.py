from flask import Flask, Response, redirect, request
import requests
import os


app = Flask(__name__)

@app.route('/')
def redirect_to_google_oauth_login():
    redirect_url = 'https://accounts.google.com/o/oauth2/auth'
    query_params = {
        'response_type': 'code',
        'client_id': os.environ['GOOGLE_OAUTH_CLIENT_ID'],
        'redirect_uri': 'https://conrad.pythonanywhere.com/oauth2callback',
        # for the scopes, check it out at https://developers.google.com/oauthplayground/
        'scope': 'https://www.googleapis.com/auth/userinfo.email',
        ## 'access_type': 'offline',
        'state': 'lalalalal1',
    }
    final_url = requests.Request(url=redirect_url, params=query_params).prepare().url
    return redirect(final_url)

@app.route('/oauth2callback')
def google_oauth2_authcode_callback():
    if 'error' in request.args:
        return Response('oh so sad')
    # get access token and refresh token using the auth code
    auth_code = request.args['code']
    # check your google config json for which link to swap auth-code for token
    oauth_link = 'https://accounts.google.com/o/oauth2/token'
    post_params = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'client_id': os.environ['GOOGLE_OAUTH_CLIENT_ID'],
        'client_secret': os.environ['GOOGLE_OAUTH_CLIENT_SECRET'],
        'redirect_uri': 'https://conrad.pythonanywhere.com/oauth2callback',
        # the same redirect_uri used to generate the authcode
    }
    result = requests.post(oauth_link, data=post_params).json()
    access_token = result['access_token']  # also has other stuff like token_id

    google_plus_user_info_api = 'https://www.googleapis.com/userinfo/v2/me'
    hidden_headers = {'Authorization': 'Bearer {}'.format(access_token)}
    user_info = requests.get(google_plus_user_info_api, headers=hidden_headers).json()
    return Response('cool- your email is {}'.format(user_info['email']))


