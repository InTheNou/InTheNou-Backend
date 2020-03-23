from app import app
from flask import Flask , redirect ,url_for,session,jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from app.handlers.UserHandler import UserHandler
from flask_login import login_required, logout_user
from app.oauth import admin_role_required, mod_role_required


##APP ROUTES##

@app.route("/App/Users/uid=<int:uid>", methods=['GET'])
@login_required
@mod_role_required
def getUserByID(uid):
    if request.method == 'GET' : return UserHandler().getUserByID(uid=uid)
    else: return jsonify(Error='Method not allowed.'), 405







