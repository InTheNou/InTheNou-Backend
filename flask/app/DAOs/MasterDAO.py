import psycopg2
from app import config
class MasterDAO:
    """
    Master DAO class from which all DAO classes inherit their connection
    to the PostgresSQL database using psycopg2.
    """
    def __init__(self):
        """
        Initializes the MasterDAO object.
        Used to give the inheriting classes their connections to the
        database.

        :var connection_url: string containing the parameters to connect to the database.
            Gets the values from :class:`app.config`
        :var self.conn: psycopg2 connection object.
        """
        connection_url = "dbname=%s user=%s password=%s host=%s port=%s" % (config.POSTGRES_DB,
                                                                    config.POSTGRES_USER,
                                                                    config.POSTGRES_PW,
                                                                    config.POSTGRES_HOSTNAME,
                                                                    config.POSTGRES_PORT)
        self.conn = psycopg2._connect(connection_url)