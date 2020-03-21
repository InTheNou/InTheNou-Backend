import psycopg2
from app import config
class MasterDAO:
    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (config.POSTGRES_DB,
                                                                    config.POSTGRES_USER,
                                                                    config.POSTGRES_PW,
                                                                    config.POSTGRES_URL,
                                                                    config.POSTGRES_PORT)
        self.conn = psycopg2._connect(connection_url)