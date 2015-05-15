from flask import Flask, Response, redirect, request
from requests import Request


app = Flask(__name__)

@app.route('/')
def redirect_to_google_oauth_login():
    redirect_url = 'https://accounts.google.com/o/oauth2/auth'
    query_params = {
        'response_type': 'code',
        'client_id': os.environ['GOOGLE_OAUTH_CLIENT_ID'],
        'redirect_uri': 'https://conrad.pythonanywhere.com/oauth2callback',
        'scope': 'email',
    }
    final_url = Request(url=redirect_url, params=query_params).prepare().url
    return redirect(final_url)

@app.route('/oauth2callback')
def google_callback():
    if 'error' in request.args:
        return Response('oh so sad')
    else:
        return Response('cool- got key ending with {}'.format(request.args['code'][-5:]))