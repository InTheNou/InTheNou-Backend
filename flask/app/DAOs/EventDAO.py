from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql

class EventDAO(MasterDAO):

    def getEventByID(self, eid):
        """
        Query Database for an Event's information by its eid.
        Parameters:
            eid: event ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('eid'),
                sql.Identifier('ecreator'),
                sql.Identifier('roomid'),
                sql.Identifier('etitle'),
                sql.Identifier('edescription'),
                sql.Identifier('estart'),
                sql.Identifier('eend'),
                sql.Identifier('ecreation'),
                sql.Identifier('estatus'),
                sql.Identifier('estatusdate'),
                sql.Identifier('photourl')
            ]),
            table1=sql.Identifier('events'),
            table2=sql.Identifier('photos'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'),
            pkey=sql.Identifier('eid'))
        cursor.execute(query, (eid,))
        result = cursor.fetchone()
        return result

    def getUpcomingGeneralEventsSegmented(self, offset, limit):
        """
         Query Database for events that are active, that have not ended,
            ordered by closest start date, offset by a set number of rows,
             returning a limited number of rows after offset.
        Parameters:
            offset: Number of rows to ignore from top results.
            limit: Maximum number of rows to return from query results.
        Returns:
            List[Tuple]: SQL result of Query as a list of tuples.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "where {pkey1}= %s and {pkey2} > CURRENT_TIMESTAMP "
                        "order by {table1Identifier2}"
                        "offset %s"
                        "limit %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('eid'),
                sql.Identifier('ecreator'),
                sql.Identifier('roomid'),
                sql.Identifier('etitle'),
                sql.Identifier('edescription'),
                sql.Identifier('estart'),
                sql.Identifier('eend'),
                sql.Identifier('ecreation'),
                sql.Identifier('estatus'),
                sql.Identifier('estatusdate'),
                sql.Identifier('photourl')
            ]),
            table1=sql.Identifier('events'),
            table2=sql.Identifier('photos'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'),
            pkey1=sql.Identifier('estatus'),
            pkey2=sql.Identifier('eend'),
            table1Identifier2=sql.Identifier('estart'))
        cursor.execute(query, ('active', int(offset), int(limit)))
        result = []
        for row in cursor:
            result.append(row)
        return result

