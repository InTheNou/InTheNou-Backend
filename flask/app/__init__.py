import os
from flask import Flask , redirect ,url_for
from flask_dance.contrib.google import make_google_blueprint, google
from dotenv import load_dotenv
load_dotenv()

app = Flask (__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersekrit")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
google_bp = make_google_blueprint(scope=["profile", "email"], offline=True)
app.register_blueprint(google_bp, url_prefix="/login")

from app import routes