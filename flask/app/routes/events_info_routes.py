from app import app
from flask import Flask , redirect ,url_for,session,jsonify
from flask_dance.contrib.google import make_google_blueprint, google
from app.handlers.EventHandler import EventHandler

@app.route("/hello")
def hello():
    # return "howdy."
    return EventHandler().getEventByID(3)
