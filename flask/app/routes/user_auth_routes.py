from app import app
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.requests import OAuth1Session
from flask import Flask , redirect ,url_for,flash, render_template,session
from flask_login import login_required, logout_user



#route used to logout user, must be logged in to access
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("app_home"))

@app.route("/App/login")
# @authorization_required
def app_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    return render_template("home.html")


# @app.route("/")
# @login_required
# def index():
#     return render_template("home.html")


#home route, redirects to template for home, there it checks if user is logged in or not, has to be changed
@app.route("/App/home")
def app_home():
    return render_template("home.html")


############## Google oAuth Test routes ##############
# @app.route("/")
# def index():
#     if not google.authorized:
#         return redirect(url_for("google.login"))
#     token =session.get('google_oauth_token')
#     print (token.get('id_token'))    
#     resp = google.get("/oauth2/v2/userinfo")
#     assert resp.ok, resp.text
#     return resp.content


# @app.route ("/login")
# def login():
#         return "Hello World, from a container"


# @app.route ("/logged")
# def logged():
#         return "You have been taken here, after the googe log in !!!"


################## DASHBOARD ROUTES ######################


@app.route("/Dashboard/login")
def dashboard_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    return render_template("home.html")

    