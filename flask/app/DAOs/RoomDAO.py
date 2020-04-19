from app.DAOs.MasterDAO import MasterDAO
from app.DAOs.AuditDAO import AuditDAO

from psycopg2 import sql


class RoomDAO(MasterDAO):
    def roomInfoArgs(self, roomKeys):
        """
        """

        fields = []
        for key in roomKeys:
            fields.append(key + " = " + str(roomKeys[key]))
        return fields

    def getRoomByID(self, rid):
        """
         Query Database for an Room's information by its rid.
        Parameters:
            rid: event ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "where {pkey}= %s;").format(
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
                sql.Identifier('photourl')
            ]),
            table1=sql.Identifier('rooms'),
            table2=sql.Identifier('photos'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'),
            pkey=sql.Identifier('rid'))
        cursor.execute(query, (int(rid),))
        result = cursor.fetchone()
        return result

    def getRoomsByBuildingAndFloor(self, bid, rfloor):
        """
         Query Database for all the rooms on a given building's floor..
        Parameters:
            bid: building ID
            rfloor: room floor
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "where {pkey1}= %s and {pkey2}= %s"
                        "order by {orderkey};").format(
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
                sql.Identifier('photourl')
            ]),
            table1=sql.Identifier('rooms'),
            table2=sql.Identifier('photos'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'),
            pkey1=sql.Identifier('bid'),
            pkey2=sql.Identifier('rfloor'),
            orderkey=sql.Identifier('rcode'))
        cursor.execute(query, (int(bid), int(rfloor)))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def changeRoomCoordinates(self, rid, roomKeys, uid):
        cursor = self.conn.cursor()
        fields_list = self.roomInfoArgs(roomKeys=roomKeys)

        audit = AuditDAO()
        tablename = "rooms"
        pkey = "rid"
        oldValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=rid, cursor=cursor)

        query = sql.SQL("update {table1} set {fields}  "
                        "where  {pkey1} = %s  "
                        "returning rid,rcode,rfloor,rlongitude,rlatitude,raltitude ").format(
            table1=sql.Identifier('rooms'),
            fields=sql.SQL(",").join(map(sql.SQL, fields_list)),
            pkey1=sql.Identifier('rid'))
        cursor.execute(query, (int(rid), ))
        result = cursor.fetchone()

        newValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=rid, cursor=cursor)
        audit.insertAuditEntry(changedTable=tablename, changeType=audit.UPDATEVALUE, oldValue=oldValue,
                               newValue=newValue, uid=uid, cursor=cursor)
        self.conn.commit()

        if result is None:
            return None
        else:
            return result

    def getRoomsByKeywordSegmented(self, keywords, offset, limit):
        """
         Query Database for an Room's information by description keywords.
        Parameters:
            keywords: string of keywords separated by a pipe "|"
            offset: Number of rows to ignore from top results.
            limit: Maximum number of rows to return from query results.
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "where rdescription_tokens @@ to_tsquery('spanish', %s) "
                        "or rdescription_tokens @@ to_tsquery(%s)"
                        "offset %s "
                        "limit %s;").format(
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
                sql.Identifier('photourl')
            ]),
            table1=sql.Identifier('rooms'),
            table2=sql.Identifier('photos'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'),
            pkey=sql.Identifier('rid'))
        cursor.execute(query, (str(keywords), str(
            keywords), int(offset), int(limit)))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # TODO: IMPLEMENT THE PROPER QUERY
    def getRoomsByCodeSearchSegmented(self, babbrev, rcode, offset, limit):
        """
         Query Database for an Room's information by description keywords.
        Parameters:
            keywords: string of keywords separated by a pipe "|"
            offset: Number of rows to ignore from top results.
            limit: Maximum number of rows to return from query results.
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        babbrev = '%' + babbrev + '%'
        rcode = '%' + rcode + "%"
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from ("
                        "select rid, rooms.bid, rcode, "
                        "rfloor, rdescription, roccupancy, "
                        "rdept, rcustodian, rlongitude, rlatitude, "
                        "raltitude, rooms.photoid "
                        "from rooms "
                        "left join buildings "
                        "on rooms.bid=buildings.bid "
                        "where (babbrev like %s and rcode like %s) "
                        "or rcode like %s) as fr "
                        "left outer join photos "
                        "on fr.photoid=photos.photoid "
                        "offset %s "
                        "limit %s;").format(
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
                sql.Identifier('photourl')
            ]))
        cursor.execute(query, (str(babbrev), str(rcode), str(
            babbrev+rcode), int(offset), int(limit)))
        result = []
        for row in cursor:
            result.append(row)
        return result
