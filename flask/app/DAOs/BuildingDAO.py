from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql


class BuildingDAO(MasterDAO):

    def getBuildingByID(self, bid):
        """
                Query Database for an Building's information by its bid.
               Parameters:
                   bid: building ID
               Returns:
                   Tuple: SQL result of Query as a tuple.
               """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('bid'),
                sql.Identifier('bname'),
                sql.Identifier('numfloors'),
                sql.Identifier('bcommonname'),
                sql.Identifier('btype'),
                sql.Identifier('photourl')
            ]),
            table1=sql.Identifier('buildings'),
            table2=sql.Identifier('photos'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'),
            pkey=sql.Identifier('bid'))
        cursor.execute(query, (int(bid),))
        result = cursor.fetchone()
        return result
