import os
from dotenv import load_dotenv
load_dotenv()

POSTGRES_PORT = os.getenv("DATABASE_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PW = os.getenv("POSTGRES_PW")
POSTGRES_DB = os.getenv("POSTGRES_DB")
try:
    POSTGRES_URL = os.environ['HOSTNAME']
except KeyError:
    POSTGRES_URL = os.getenv("DATABASE_URL")

DB_URI = 'postgresql+psycopg2://{user}:{pw}@{url}:{port}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,port=POSTGRES_PORT,db=POSTGRES_DB)


class Config(object):
    SECRET_KEY= os.getenv("FLASK_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")