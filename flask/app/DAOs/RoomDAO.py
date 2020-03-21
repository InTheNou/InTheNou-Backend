from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql


class RoomDAO(MasterDAO):

    def getRoomByID(self, rid):
        """
         Query Database for an Room's information by its rid.
        Parameters:
            rid: event ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table} where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('rid'),
                sql.Identifier('bid'),
                sql.Identifier('rcode'),
                sql.Identifier('rfloor'),
                sql.Identifier('rdescription'),
                sql.Identifier('roccupancy'),
                sql.Identifier('rdept'),
                sql.Identifier('rcustodian'),
                sql.Identifier('rlongitude'),
                sql.Identifier('rlatitude'),
                sql.Identifier('raltitude'),
                sql.Identifier('photoid')
            ]),
            table=sql.Identifier('rooms'),
            pkey=sql.Identifier('rid'))
        cursor.execute(query, (int(rid),))
        result = cursor.fetchone()
        return result
