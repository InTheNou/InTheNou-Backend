from functools import wraps
from flask import g, flash, redirect, url_for, flash, render_template, session
from flask_login import current_user, login_user
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from .models import db, User, OAuth
from app.handlers.UserHandler import UserHandler


# FLASK-DANCE setup, need to fix offline setting so that we can refresh sessions if user token expires
blueprint = make_google_blueprint(
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(
        OAuth, db.session, user_required=False, user=current_user),

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

    user_id = info["id"]
    print("Got User")
    # Find this OAuth token in the database, or create it
    query = User.query.filter_by(provider=user_id)
    try:

        user = query.one()
    except NoResultFound:
        user = User(
            email=info["email"],
            provider=user_id,
            first_name=info["given_name"],
            last_name=info["family_name"],
            user_type="Student",
            user_role=int(1),
            role_issuer=int(1),

        )

        # Save and commit our database models
        db.session.add_all([user])
        db.session.commit()
        oauth = OAuth(provider=blueprint.name,
                      id=(user.id), token=str(token))

        db.session.add_all([oauth])
        db.session.commit()

    if user is not None:
        query = OAuth.query.filter_by(id=user.id)
        try:
            print("lookin 4 token")
            oauth = query.one()
        except NoResultFound:

            oauth = OAuth(provider=blueprint.name,
                          id=user.id, token=str(token))
            db.session.add_all([oauth])
            db.session.commit()

        login_user(oauth.user)
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
