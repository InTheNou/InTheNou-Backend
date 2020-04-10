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

   # print (token)
    newAccount = False
    user_usub = info["id"]
    # Find this google id in the database, or create it
    query = User.query.filter_by(provider=user_usub)
    try:

        user = query.one()
    except NoResultFound:
        print("No user found")
        if session['AppLogin'] == True:
            # Create account for new user
            print("User being creted")
            newAccount = True
            user = User(email=info["email"],
                        provider=user_usub,
                        first_name=info["given_name"],
                        last_name=info["family_name"],
                        user_type="Student",
                        user_role=int(1),
                        role_issuer=int(1),
                        )
            if(user):
                db.session.add_all([user])
                db.session.commit()
        else:
            flash("User must create account in the InTheNou App")
            return (redirect(url_for("dashboard_home")))

    # user was found in the database
    print("looking for Token")
    query = OAuth.query.filter_by(
        token=str(token['access_token']), user=user, id=user.id)
    try:
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

    sessionDict = str(session)[20:-1]

    # print(sessionDict)
    # {'_fresh': True, '_id': '934028cbba09af9ef6c35734f503a02c84a5f9d54e92c85bd1b3c7b0eb9167791a93fe9cf0a6a57c1af31d4d319031a244a2514124fa970b7ebb39d06249737f', '_user_id': '2', 'token': 'ya29.a0Ae4lvC25jHQPYb40hlyWPdxeVpgE8lPKEhYURwbfNkWdfO-4z4joM3zZByq1UlFdXbjt5y40-qYGy3lClOL6ffCyWRIYIBfgbia-vKBpA5Aspd5LNNIueAJI-zlO04k-vPHYUxmP2r3imNF33avaI3Xe0-3jSS-yOrNV"}
    cookie = encodeFlaskCookie(secret_key=os.getenv(
        "FLASK_SECRET_KEY"), cookieDict=sessionDict)
    # print(cookie)
    session['cookys'] = cookie
    #print(decodeFlaskCookie(secret_key=os.getenv("FLASK_SECRET_KEY"), cookieValue=cookie))
    print('Session Checking')

    if(session['AppLogin'] == True):
        print('session True!')
        return redirect('inthenou://succsess?uid=' + str(user.id)+'&newAccount='+str(newAccount)+'&cookie='+cookie)
    else:
        print('session False!')
        return (jsonuser)


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
