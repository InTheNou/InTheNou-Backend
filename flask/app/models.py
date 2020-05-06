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
    """
    Class containing all the methods used to build and execute queries to
    the database for requests concerning user authentication and account creation.   
    """
    __tablename__ = 'users'
    id = db.Column("uid", db.Integer, primary_key=True)
    """
    The uid of the User 
     
    """
    email = db.Column(db.String(256), unique=True)
    """
    The email of the user
  
    
    """
    provider = db.Column("usub", db.String(256), unique=True, nullable=False)
    """
    The name of the authentication provider
    
    """
    display_name = db.Column("display_name", db.String(256), unique=False)
    """
    The display name of the user, given by the authentication provider
  
    """
    user_type = db.Column("type", db.String(256), unique=False)
    """
    The type of user, at the moment it is default to 'student'
    
    """
    user_role = db.Column("roleid", db.Integer, unique=False)
    """
    
    The role id for the user
     
    """
    role_issuer = db.Column("roleissuer", db.Integer, unique=False)
    """
    
    The uid of the user that delegated this user a role
    
    """

class OAuth(db.Model):
    """
    Class containing all the methods used to build and execute queries to
    the database for requests concerning user authentication tokens and sessions
    """
    __tablename__ = 'oauth'
    token = db.Column('access_token', primary_key=True)
    """
    The access_token from the authoentication provider
    
    """
    id = db.Column("uid", db.Integer, db.ForeignKey(
        User.id), nullable=False, primary_key=True)
    """
    The uid of the user asociated with this access_token/session
    
    """
    provider = db.Column(db.String(256), unique=False, nullable=False)
    """
    The name of the authentication provider
    
    """
    user = db.relationship(User)
    """
    Relation to the users table
    
    """


# Login Manager
login_manager = LoginManager()
"""
Class for hanlding loggin in, part of flask_login
"""
login_manager.login_view = "google.login"
"""
Configuration for login authentication (flask_login_)
"""

# FLASK-Login manager, gets a user id and search for id in the database
@login_manager.user_loader
def load_user(id):
    """
    Method to access the database, returns a user , given a uid
    """
    return User.query.get(int(id))
