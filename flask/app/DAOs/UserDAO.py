from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql

class UserDAO(MasterDAO):
     
    def getUserByID(self, uid):
        """
        Query Database for an User's information by his/her uid.
        Parameters:
            uid: user ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('uid'),
                sql.Identifier('email'),
                sql.Identifier('first_name'),
                sql.Identifier('last_name'),
                sql.Identifier('type'),
                sql.Identifier('roleid')
            ]),
            table1=sql.Identifier('users'),
            pkey=sql.Identifier('uid'))
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
        return result