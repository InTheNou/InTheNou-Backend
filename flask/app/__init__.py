from flask import Flask , redirect ,url_for, flash, render_template
from flask_login import login_required, logout_user
from .config import Config,DB_URI
from .models import db, login_manager
from .oauth import blueprint
from .cli import create_db
from flask_sqlalchemy import SQLAlchemy



app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =DB_URI
app.config.from_object(Config)
app.register_blueprint(blueprint, url_prefix="/login")


db.init_app(app)
login_manager.init_app(app)


from app import routes
