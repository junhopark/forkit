from flask import Flask, request, redirect, render_template, flash
from flask_github import GitHub
import requests
import os
import json


def _read_secrets() -> dict:
    filename = os.path.join('secrets.json')
    try:
        with open(filename, mode='r') as file:
            return json.loads(file.read())
    except FileNotFoundError:
        return {}


app = Flask(__name__)

secrets = _read_secrets()
app.secret_key = secrets["FLASK_SECRET_KEY"]

CLIENT_ID = secrets["GITHUB_CLIENT_ID"]
REPO_URL = "https://api.github.com/repos/junhopark/forkit/forks"

if __name__ == '__main__':
    app.run()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return redirect('https://github.com/login/oauth/authorize?client_id=%s&scope=repo' % CLIENT_ID)


@app.route('/oauth-callback')
def oauth_callback():
    code = request.args.get('code')

    oauth_token = _get_access_token(secrets["GITHUB_CLIENT_SECRET"], code)

    if oauth_token is None:
        flash("Authorization failed")
    else:
        response = requests.post(
            REPO_URL,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": 'Bearer %s' % oauth_token
            }
        )
        if (response.status_code == 202):
            flash("Success!")
        else:
            flash("Error occurred")

    return render_template('index.html')


def _get_access_token(client_secret, request_token) -> str:
    if not CLIENT_ID or not client_secret or not request_token:
        raise ValueError(
            'CLIENT_ID, client_secret, request_token need to be supplied')

    response = requests.post(
        f'https://github.com/login/oauth/access_token?client_id={CLIENT_ID}&client_secret={client_secret}&code={request_token}',
        headers={
            'accept': 'application/vnd.github+json'
        }
    )

    try:
        return response.json()['access_token']
    except:
        return None
