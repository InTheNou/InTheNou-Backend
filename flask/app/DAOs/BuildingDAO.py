from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql
from psycopg2.extensions import AsIs


class BuildingDAO(MasterDAO):
    def getAllBuildingsSegmented(self, limit, offset):
        """
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "offset %s limit %s ").format(
            fields=sql.SQL(',').join([
                sql.Identifier('bid'),
                sql.Identifier('bname'),
                sql.Identifier('babbrev'),
                sql.Identifier('numfloors'),
                sql.Identifier('bcommonname'),
                sql.Identifier('btype'),
                sql.Identifier('photourl')
            ]),
            table1=sql.Identifier('buildings'),
            table2=sql.Identifier('photos'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'))
        cursor.execute(query, (offset, limit))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllBuildings(self):
        """
                Query Database for all Building entries.
               Returns:
                   Tuple: SQL result of Query as a tuple.
               """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier};").format(
            fields=sql.SQL(',').join([
                sql.Identifier('bid'),
                sql.Identifier('bname'),
                sql.Identifier('babbrev'),
                sql.Identifier('numfloors'),
                sql.Identifier('bcommonname'),
                sql.Identifier('btype'),
                sql.Identifier('photourl')
            ]),
            table1=sql.Identifier('buildings'),
            table2=sql.Identifier('photos'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'))
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

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
                sql.Identifier('babbrev'),
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

    def getDistinctFloorNumbersByBuildingID(self, bid):
        cursor = self.conn.cursor()
        query = sql.SQL("select distinct rfloor "
                        "from {table} "
                        "where {pkey}=%s "
                        "order by rfloor;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('rfloor')
            ]),
            table=sql.Identifier('rooms'),
            pkey=sql.Identifier('bid'))
        cursor.execute(query, (int(bid),))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def searchBuildingsByKeyword(self, offset, limit, keyword):
        keyword = "'%" + keyword + "%'"
        keyword = AsIs(keyword)
        print(keyword)
        cursor = self.conn.cursor()
        query = sql.SQL("select distinct {fields} "
                        "from {table} join {table2} "
                        "on photos.photoid = buildings.photoid "
                        "where ( bname like UPPER ( %s  ) or babbrev like UPPER ( %s  ) ) "
                        "offset %s limit %s ").format(
            fields=sql.SQL(',').join([
                sql.Identifier('bid'),
                sql.Identifier('bname'),
                sql.Identifier('babbrev'),
                sql.Identifier('btype'),
                sql.Identifier('photourl')
            ]),
            table=sql.Identifier('buildings'),
            table2=sql.Identifier('photos'))
        cursor.execute(query, ((keyword), (keyword), offset, limit))
        result = []
        for row in cursor:
            result.append(row)
        return result
