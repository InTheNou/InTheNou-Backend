from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql


class TagDAO(MasterDAO):

    def getTagByID(self, tid):
        """
         Query Database for an Tag's information by its tid.
        Parameters:
            tid: tag ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('tid'),
                sql.Identifier('tname')
            ]),
            table=sql.Identifier('tags'),
            pkey=sql.Identifier('tid'))
        cursor.execute(query, (int(tid),))
        result = cursor.fetchone()
        return result
