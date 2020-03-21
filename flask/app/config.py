import os
from dotenv import load_dotenv
load_dotenv()

#variables from .env used to build database URI for psycopg2 
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PW = os.getenv("POSTGRES_PW")
POSTGRES_DB = os.getenv("POSTGRES_DB")
try:
    POSTGRES_HOSTNAME = os.environ['POSTGRES_CONTAINER']
except KeyError:
    POSTGRES_HOSTNAME = os.getenv("POSTGRES_LOCAL")

DB_URI = 'postgresql+psycopg2://{user}:{pw}@{hostname}:{port}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,hostname=POSTGRES_HOSTNAME, port=POSTGRES_PORT,db=POSTGRES_DB)


class Config(object):
    SECRET_KEY= os.getenv("FLASK_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")