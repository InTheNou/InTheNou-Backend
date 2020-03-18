from app import app
from flask import Flask , redirect ,url_for,session,jsonify
from flask_dance.contrib.google import make_google_blueprint, google


@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    token =session.get('google_oauth_token')
    print (token.get('id_token'))    
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    return resp.content

@app.route ("/login")
def login():
        return "Hello World, from a container"


@app.route ("/logged")
def logged():
        return "You have been taken here, after the google log in !!!"