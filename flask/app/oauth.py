from flask import flash
from flask_login import current_user, login_user
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from .models import db, User


blueprint = make_google_blueprint(
    scope=["profile", "email"],
    storage=SQLAlchemyStorage(User, db.session, user=current_user),
    offline=True
)

#create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in.", category="error")
        return False

    resp = blueprint.session.get("/oauth2/v1/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info."
        flash(msg, category="error")
        return False

    info = resp.json()
    print (info)
    user_id = info["id"]
    # Find this OAuth token in the database, or create it
    query = User.query.filter_by( provider_user_id=user_id)
    try:
        user = query.one()
    except NoResultFound:
        user = User(provider_user_id=user_id)

    if user.id:
        login_user(user)
        flash("Successfully signed in.")

    else:
        # Create a new local user account for this user
        user = User(email=info["email"],provider_user_id=info["id"],
         first_name=info["given_name"],
          last_name=info["family_name"],
          user_type="Student",
          user_role= int(1),
          role_issuer=int(1)
          )
        # Associate the new local user account with the OAuth token
       # user.user = user
        # Save and commit our database models
        db.session.add_all([user])
        db.session.commit()
        # Log in the new local user account
        login_user(user)
        flash("Successfully signed in.")

    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False


# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def google_error(blueprint, message, response):
    msg = ("OAuth error from {name}! " "message={message} response={response}").format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")
