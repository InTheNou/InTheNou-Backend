from functools import wraps
from flask import g,flash,redirect ,url_for,flash, render_template,session
from flask_login import current_user, login_user
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from .models import db, User
from app.handlers.UserHandler import UserHandler


#FLASK-DANCE setup, need to fix offline setting so that we can refresh sessions if user token expires
blueprint = make_google_blueprint(
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(User, db.session,user_required=False, user=current_user),
    offline=True
)

#create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    #if no token was recieved from google, throw error 
    if not token:
        flash("Failed to log in.", category="error")
        return False
    #request user information by providing google with Token
    resp = blueprint.session.get("/oauth2/v1/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False
    #Decrypt JSON token from Google oAuth 
    info = resp.json()
    
    
    user_usub = info["id"]
    # Find this google id in the database, or create it
    query = User.query.filter_by( provider=user_usub)
    try:
        user = query.one()
    #user was not found in the database
    except NoResultFound:
        user = User(provider=user_usub)
    #user was found in the database
    if user.id:
        login_user(user)
        flash("Successfully signed in.")
    # Create a new local user account for this user, "hardcoded type,role and role issuer attributes"
    else:
        user = User(
          email=info["email"],
          provider=user_usub,
          first_name=info["given_name"],
          last_name=info["family_name"],
          user_type="Student",
          user_role= int(1),
          role_issuer=int(1),
          
          )
       
        # Save and commit our database models
        db.session.add_all([user])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in.")
        
    
    return UserHandler().getUserByID(int(user.id))


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