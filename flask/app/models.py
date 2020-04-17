from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

# data base object from FLASK-SQLAlchemy
db = SQLAlchemy()

token = {}
# User object for FLASK-SQLAlchemy and Flask-Login

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column("uid", db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    provider = db.Column("usub", db.String(256), unique=True, nullable=False)
    display_name = db.Column("display_name", db.String(256), unique=False)
    user_type = db.Column("type", db.String(256), unique=False)
    user_role = db.Column("roleid", db.Integer, unique=False)
    role_issuer = db.Column("roleissuer", db.Integer, unique=False)


class OAuth(db.Model):
    __tablename__ = 'oauth'
    token = db.Column('access_token', primary_key=True)
    created_at = db.Column(db.String(256))
    id = db.Column("uid", db.Integer, db.ForeignKey(
        User.id), nullable=False, primary_key=True)
    provider = db.Column(db.String(256), unique=False, nullable=False)
    user = db.relationship(User)


# Login Manager
login_manager = LoginManager()
login_manager.login_view = "google.login"

# FLASK-Login manager, gets a user id and search for id in the database
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
