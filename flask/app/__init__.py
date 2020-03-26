from flask import Flask , redirect ,url_for, flash, render_template
from flask_login import login_required, logout_user
from .config import Config,DB_URI
from .models import db, login_manager
from .oauth import blueprint
from flask_sqlalchemy import SQLAlchemy


app = Flask (__name__)
#configure Database URL for Psycopg2
app.config['SQLALCHEMY_DATABASE_URI'] =DB_URI
#configure enviroment variables located in config file 
app.config.from_object(Config)
#create google oAuth login Blueprint
app.register_blueprint(blueprint, url_prefix="/login")

#initialize FLASK-SQLAlchemy object and FLASK-Login object 
db.init_app(app)
login_manager.init_app(app)


from app.routes import user_info_routes,user_auth_routes,events_info_routes
