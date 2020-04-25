from itsdangerous import URLSafeTimedSerializer
from flask.sessions import SecureCookieSessionInterface
import os
from dotenv import load_dotenv
load_dotenv()


# variables from .env used to build database URI for psycopg2
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PW = os.getenv("POSTGRES_PW")
POSTGRES_DB = os.getenv("POSTGRES_DB")

try:
    POSTGRES_HOSTNAME = os.environ['POSTGRES_CONTAINER']
except KeyError:
    POSTGRES_HOSTNAME = os.getenv("POSTGRES_LOCAL")

DB_URI = 'postgresql+psycopg2://{user}:{pw}@{hostname}:{port}/{db}'.format(
    user=POSTGRES_USER, pw=POSTGRES_PW, hostname=POSTGRES_HOSTNAME, port=POSTGRES_PORT, db=POSTGRES_DB)


class Config(object):
    """
    Configuration file that handles setting global variables for data access/connections.

    :var: SECRET_KEY
    :var: SQLALCHEMY_TRACK_MODIFICATIONS
    :var: GOOGLE_OAUTH_CLIENT_ID
    :var: GOOGLE_OAUTH_CLIENT_SECRET
    """
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")


class SimpleSecureCookieSessionInterface(SecureCookieSessionInterface):
    # Override method
    # Take secret_key instead of an instance of a Flask app
    def get_signing_serializer(self, secret_key):
        if not secret_key:
            return None
        signer_kwargs = dict(
            key_derivation=self.key_derivation,
            digest_method=self.digest_method
        )
        return URLSafeTimedSerializer(secret_key, salt=self.salt,
                                      serializer=self.serializer,
                                      signer_kwargs=signer_kwargs)


def decodeFlaskCookie(secret_key, cookieValue):
    sscsi = SimpleSecureCookieSessionInterface()
    signingSerializer = sscsi.get_signing_serializer(secret_key)
    return signingSerializer.loads(cookieValue)

# Keep in mind that flask uses unicode strings for the
# dictionary keys


def encodeFlaskCookie(secret_key, cookieDict):
    sscsi = SimpleSecureCookieSessionInterface()
    signingSerializer = sscsi.get_signing_serializer(secret_key)
    return signingSerializer.dumps(cookieDict)
