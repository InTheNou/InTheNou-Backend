from functools import wraps
from flask import g, flash, redirect, url_for, flash, render_template, session, request, jsonify
from flask_login import current_user, login_user
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from .models import db, User, OAuth
from .config import *
from app.handlers.UserHandler import UserHandler

# FLASK-DANCE setup, need to fix offline setting so that we can refresh sessions if user token expires
blueprint = make_google_blueprint(
    reprompt_select_account=True,
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(
        OAuth, db.session, user_required=True, user=current_user),
    offline=True
)

# create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    # if no token was recieved from google, throw error
    if not token:
        flash("Failed to log in.", category="error")
        return False
    # request user information by providing google with Token
    print("checking sessions")
    resp = blueprint.session.get("/oauth2/v1/userinfo")

    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False
    # Decrypt JSON token from Google oAuth
    info = resp.json()
      # user was found in the database
    print(token)
    display_name = info['given_name']+" "+ info['family_name']
    session['token']=token
    user_usub = info["id"]
    # Find this google id in the database, or create it
    query = User.query.filter_by(provider=user_usub)
    try:
        user = query.one()
    except NoResultFound:
            print("User being created")
            user = User(email=info["email"],
                    provider=user_usub,
                    display_name=display_name,
                    user_type="Student",
                    user_role=int(1),
                    role_issuer=int(1),
                    )
            if(user):
                db.session.add_all([user])
                db.session.commit()
            
            print("USER CAN NOT BE CREATED ERROR CODE  =  0 ")
            flash("User must create account in the InTheNou App")
            
            response = redirect("http://localhost:8080/#/login/fail/?error=0") 
            return response
  
    try:
        if int(user.user_role) < 3:
            response = redirect("http://localhost:8080/#/login/fail/?error=1") 
            return response
        
        query = OAuth.query.filter_by(
            token=str(token['access_token']), user=user, id=user.id)
        oauth = query.one()
    # user was not found in the database
    except NoResultFound:
        if(user):
            oauth = OAuth(provider=blueprint.name, token=str(token['access_token']), created_at=(
                str(token['expires_at'])), id=user.id, user=user)
            session['token'] = str(token['access_token'])
            db.session.add_all([oauth])
            db.session.commit()

            if(oauth.user):
                login_user(oauth.user)
                flash("Successfully signed in.")
                jsonuser = UserHandler().getUserByID(int(user.id))

                response = redirect("http://localhost:8080/#/login/succeed/?uid="+str(user.id)) 
                return response
    


# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def google_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")


def admin_role_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.user_role == 4:
            return f(*args, **kwargs)
        else:
            flash("You need to be an admin for this action.")
            return redirect(url_for('app_home'))

    return wrap


def mod_role_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.user_role >= 3:
            return f(*args, **kwargs)
        else:
            flash("You need to be a moderator for this action.")
            return redirect(url_for('app_home'))

    return wrap


def event_creator_role_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.user_role >= 2:
            return f(*args, **kwargs)
        else:
            flash("You need to be a event creator for this action.")
            return redirect(url_for('app_home'))
    return wrap


def token_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            session['token'] = str(session['token'])
            return f(*args, **kwargs)
        except:
            flash("You need to be authorized to use this function yo.")

    return wrap
