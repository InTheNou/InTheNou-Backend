from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql, errors


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
        cursor.execute(query, (int(eid),))
        result = cursor.fetchone()
        return result

    # TODO: add UID to this, to return interaction info.
    def getUpcomingGeneralEventsSegmented(self, uid, offset, limit):
        """
         Query Database for events that are active, that have not ended,
            ordered by closest start date, offset by a set number of rows,
             returning a limited number of rows after offset.
        Parameters:
            uid: user ID.
            offset: Number of rows to ignore from top results.
            limit: Maximum number of rows to return from query results.
        Returns:
            List[Tuple]: SQL result of Query as a list of tuples.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from ("
                        "(select * from events "
                        "where estatus='active' and eend>CURRENT_TIMESTAMP "
                        "and eid not in("
                        "select eid from eventuserinteractions "
                        "where uid=%s and itype='dismissed')) "
                        "as uevents	"
                        "left outer join photos "
                        "on uevents.photoid = photos.photoid) "
                        "as undismissed_events "
                        "left outer join ("
                        "select * from eventuserinteractions "
                        "where uid=%s) "
                        "as users_interactions "
                        "on undismissed_events.eid = users_interactions.eid "
                        "order by estart "
                        "offset %s "
                        "limit %s").format(
            fields=sql.SQL(',').join([
                sql.Identifier("undismissed_events", 'eid'),
                sql.Identifier("undismissed_events", 'ecreator'),
                sql.Identifier("undismissed_events", 'roomid'),
                sql.Identifier("undismissed_events", 'etitle'),
                sql.Identifier("undismissed_events", 'edescription'),
                sql.Identifier("undismissed_events", 'estart'),
                sql.Identifier("undismissed_events", 'eend'),
                sql.Identifier("undismissed_events", 'ecreation'),
                sql.Identifier("undismissed_events", 'estatus'),
                sql.Identifier("undismissed_events", 'estatusdate'),
                sql.Identifier("undismissed_events", 'photourl'),
                sql.Identifier("users_interactions", 'itype'),
                sql.Identifier("users_interactions", 'recommendstatus')
            ]))
        cursor.execute(query, (int(uid), int(uid), int(offset), int(limit)))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUpcomingFollowedEventsSegmented(self, uid, offset, limit):
        """
         Query Database for events that the user is following, are active,
            that have not ended, ordered by closest start date, offset by
            a set number of rows, returning a limited number of rows after offset.
        Parameters:
            uid: User ID,
            offset: Number of rows to ignore from top results.
            limit: Maximum number of rows to return from query results.
        Returns:
            List[Tuple]: SQL result of Query as a list of tuples.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "natural join {table3} "
                        "where {pkey1}= %s and {pkey2} > CURRENT_TIMESTAMP "
                        "and {pkey3}=%s and {pkey4} = %s "
                        "order by {table1Identifier2} "
                        "offset %s "
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
                sql.Identifier('photourl'),
                sql.Identifier('recommendstatus')
            ]),
            table1=sql.Identifier('events'),
            table2=sql.Identifier('photos'),
            table3=sql.Identifier('eventuserinteractions'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'),
            pkey1=sql.Identifier('estatus'),
            pkey2=sql.Identifier('eend'),
            pkey3=sql.Identifier('uid'),
            pkey4=sql.Identifier('itype'),
            table1Identifier2=sql.Identifier('estart'))
        cursor.execute(query, ('active', int(uid), 'following', int(offset), int(limit)))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getDismissedEvents(self, uid, offset, limit):
        """
         Query Database for events that the user has dismissed,
          ordered by closest start date, offset by
            a set number of rows, returning a limited number of rows after offset.
        Parameters:
            uid: User ID,
            offset: Number of rows to ignore from top results.
            limit: Maximum number of rows to return from query results.
        Returns:
            List[Tuple]: SQL result of Query as a list of tuples.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "natural join {table3} "
                        "where {pkey1}= %s and {pkey2} = %s "
                        "order by {table1Identifier2} desc "
                        "offset %s "
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
                sql.Identifier('photourl'),
                sql.Identifier('recommendstatus')
            ]),
            table1=sql.Identifier('events'),
            table2=sql.Identifier('photos'),
            table3=sql.Identifier('eventuserinteractions'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'),
            pkey1=sql.Identifier('uid'),
            pkey2=sql.Identifier('itype'),
            table1Identifier2=sql.Identifier('estart'))
        cursor.execute(query, (int(uid), 'dismissed', int(offset), int(limit)))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPastFollowedEventsSegmented(self, uid, offset, limit):
        """
         Query Database for events that the user followed,
            and have ended, ordered by closest start date, offset by
            a set number of rows, returning a limited number of rows after offset.
        Parameters:
            uid: User ID,
            offset: Number of rows to ignore from top results.
            limit: Maximum number of rows to return from query results.
        Returns:
            List[Tuple]: SQL result of Query as a list of tuples.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "natural join {table3} "
                        "where {pkey1} < CURRENT_TIMESTAMP "
                        "and {pkey2}=%s and {pkey3} = %s "
                        "order by {table1Identifier2} desc "
                        "offset %s "
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
                sql.Identifier('photourl'),
                sql.Identifier('recommendstatus')
            ]),
            table1=sql.Identifier('events'),
            table2=sql.Identifier('photos'),
            table3=sql.Identifier('eventuserinteractions'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'),
            pkey1=sql.Identifier('eend'),
            pkey2=sql.Identifier('uid'),
            pkey3=sql.Identifier('itype'),
            table1Identifier2=sql.Identifier('estart'))
        cursor.execute(query, (int(uid), 'following', int(offset), int(limit)))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getEventsCreatedByUser(self, uid, offset, limit):
        """
         Query Database for events created by a user,
            ordered by highest-value start date, offset by
            a set number of rows, returning a limited number of rows after offset.
        Parameters:
            uid: User ID,
            offset: Number of rows to ignore from top results.
            limit: Maximum number of rows to return from query results.
        Returns:
            List[Tuple]: SQL result of Query as a list of tuples.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "where {pkey1}= %s "
                        "order by {table1Identifier2} desc "
                        "offset %s "
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
            pkey1=sql.Identifier('ecreator'),
            table1Identifier2=sql.Identifier('estart'))
        cursor.execute(query, (int(uid), int(offset), int(limit)))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def setInteraction(self, uid, eid, itype):
        """
         Create an eventuserinteraction entry for the defined user and event
         that sets the interaction type to the one provided, and recommended as "N". If an entry
         for the user/event key pair exists, update the itype field.
        Parameters:
            uid: User ID,
            eid: Event ID
            itype: interaction Type string
        Returns:
            List[Tuple]: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("insert into {table1} "
                        "({insert_fields}) "
                        "VALUES (%s, 'N', %s, %s) "
                        "on CONFLICT({conflict_keys}) do "
                        "update set {ukey1}= %s "
                        "returning {conflict_keys}").format(
            insert_fields=sql.SQL(',').join([
                sql.Identifier('itype'),
                sql.Identifier('recommendstatus'),
                sql.Identifier('uid'),
                sql.Identifier('eid')
            ]),
            conflict_keys=sql.SQL(',').join([
                sql.Identifier('uid'),
                sql.Identifier('eid')
            ]),
            table1=sql.Identifier('eventuserinteractions'),
            ukey1=sql.Identifier('itype'))
        try:
            cursor.execute(query, (str(itype), int(uid), int(eid), str(itype)))
            result = cursor.fetchone()
            self.conn.commit()
        except errors.ForeignKeyViolation as e:
            result = e
        return result
