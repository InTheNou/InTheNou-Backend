from app import app
from flask import Flask, g,flash,redirect ,url_for, render_template,session,request,jsonify

from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.requests import OAuth1Session
from flask_dance.consumer import oauth_before_login

from flask import Flask , redirect ,url_for,flash, render_template,session,make_response
from flask_login import login_required, logout_user,current_user
from app.models import db, User, OAuth
from app.oauth import *
from app.config import *
from sqlalchemy.orm.exc import NoResultFound
from dotenv import load_dotenv
load_dotenv()


    
    

#route used to logout user, must be logged in to access
@app.route("/App/logout")
@login_required
def app_logout():
    
    query = OAuth.query.filter_by(token=str(session['token']))
    try:
        oauth = query.one()
        db.session.delete(oauth)
        db.session.commit() 
    except NoResultFound:
        print("NO RESULT FOUND ")
    logout_user()
    flash("You have logged out")
    return render_template("home.html")
  
    
   


@app.route("/App/login")
def app_login(): 
        try:
            (current_user.id  )
            return make_response(redirect('TESTinthenou://succsess?uid='+str(current_user.id)+'&newAccount=False&cookie='+str(session['cooky'])))    
        except:
            session['AppLogin'] = True
            print('Session Defined')
            
            return redirect(url_for("google.login")) 
 

@oauth_before_login.connect
def before_google_login(blueprint, url):
    try:
        Usersession = request.headers['session']
        print("session Cached")
    except:
        print("redirecting to google")





#home route, redirects to template for home, there it checks if user is logged in or not, has to be changed
@app.route("/App/home")
def app_home():
        return redirect(url_for("google.login"))
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
#@login_required
def dashboard_login():
     
        try:
            (current_user.id  )
            return UserHandler().getUserByID(int(current_user.id))
 
              
        except:
            session['AppLogin'] = False
            print('Session Defined as '+ str(session['AppLogin']))
            #flash ("No user found ")
            return redirect(url_for("google.login")) 
        

@app.route("/Dashboard/logout")
@login_required
def dashboard_logout():
    query = OAuth.query.filter_by(token=str(session['token']))
    try:
        oauth = query.one()
        db.session.delete(oauth)
        db.session.commit() 
    except NoResultFound:
        print("NO RESULT FOUND ")
    logout_user()
    flash("You have logged out")
    return render_template("dashhome.html")

@app.route("/Dashboard/home")
def dashboard_home():
    return render_template("dashhome.html")