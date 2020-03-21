from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql

class BuildingDAO(MasterDAO):

    # def getEventByID(self, eid):
    #     cursor = self.conn.cursor()
    #     query = sql.SQL("select {fields} from {table} where {pkey}= %s;").format(
    #         fields=sql.SQL(',').join([
    #             sql.Identifier('eid'),
    #             sql.Identifier('ecreator'),
    #             sql.Identifier('roomid'),
    #             sql.Identifier('etitle'),
    #             sql.Identifier('edescription'),
    #             sql.Identifier('estart'),
    #             sql.Identifier('eend'),
    #             sql.Identifier('ecreation'),
    #             sql.Identifier('estatus'),
    #             sql.Identifier('estatusdate'),
    #             sql.Identifier('photoid')
    #         ]),
    #         table=sql.Identifier('events'),
    #         pkey=sql.Identifier('eid'))
    #     cursor.execute(query, (eid,))
    #     result = cursor.fetchone()
    #     return result
