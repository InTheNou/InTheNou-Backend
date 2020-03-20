from app import app
from flask import Flask , redirect ,url_for,flash, render_template
from flask_login import login_required, logout_user




@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("home.html")




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


