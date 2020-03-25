from app.DAOs.MasterDAO import MasterDAO
from app.DAOs.TagDAO  import TagDAO
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
                        "where {pkey1}= %s and {pkey2} = %s and {pkey3} <> %s"
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
            pkey3=sql.Identifier('estatus'),
            table1Identifier2=sql.Identifier('estart'))
        cursor.execute(query, (int(uid), 'dismissed', 'deleted', int(offset), int(limit)))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUpcomingRecommendedEventsSegmented(self, uid, offset, limit):
        """
         Query Database for events that have been recommended to the user,
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
                        "where {pkey1}= %s and {pkey2} > CURRENT_TIMESTAMP "
                        "and {pkey3}=%s and {pkey4} = %s and {pkey5} <> %s "
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
                sql.Identifier('itype')
            ]),
            table1=sql.Identifier('events'),
            table2=sql.Identifier('photos'),
            table3=sql.Identifier('eventuserinteractions'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'),
            pkey1=sql.Identifier('estatus'),
            pkey2=sql.Identifier('estart'),
            pkey3=sql.Identifier('uid'),
            pkey4=sql.Identifier('recommendstatus'),
            pkey5=sql.Identifier('itype'),
            table1Identifier2=sql.Identifier('estart'))
        cursor.execute(query, ('active', int(uid), 'R', 'dismissed', int(offset), int(limit)))
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

    def setRecommendation(self, uid, eid, recommendstatus):
        """
         Create an eventuserinteraction entry for the defined user and event
         that sets the recommendstatus to the one provided, and itype as "none". If an entry
         for the user/event key pair exists, update the itype field.
        Parameters:
            uid: User ID,
            eid: Event ID
            recommendstatus: Char that states if the event is recommended or not.
        Returns:
            List[Tuple]: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("insert into {table1} "
                        "({insert_fields}) "
                        "VALUES ('none', %s, %s, %s) "
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
            ukey1=sql.Identifier('recommendstatus'))
        try:
            cursor.execute(query, (str(recommendstatus), int(uid), int(eid), str(recommendstatus)))
            result = cursor.fetchone()
            self.conn.commit()
        except errors.ForeignKeyViolation as e:
            result = e
        return result

    def setEventStatus(self, eid, estatus):
        """
         Sets the estatus for a given event.
        Parameters:
            eid: Event ID
            estatus: string that indicates the event's status.
        Returns:
            List[Tuple]: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("update {table1} "
                        "set {ukey1} = %s "
                        "where {pkey1}= %s "
                        "returning {pkey1}").format(
            table1=sql.Identifier('events'),
            ukey1=sql.Identifier('estatus'),
            pkey1=sql.Identifier('eid'))
        try:
            cursor.execute(query, (str(estatus), int(eid)))
            result = cursor.fetchone()
            self.conn.commit()
        except errors.ForeignKeyViolation as e:
            result = e
        return result

    def createEvent(self, ecreator, roomid, etitle, edescription, estart, eend, tags, photourl, websites):
        """
        Create an Event from the information provided.
        Parameters:
            ecreator: the event creator's UID.
            roomid: the rid of the room in which the event will take place.
            etitle: the event's title string.
            edescription: the event's description string.
            estart: the event's start timestamp
            eend: the event's end timestamp which must be greater than the start timestamp.
            tags: a list of integers corresponding to tag IDs
            photourl:the url of a photo to be related to the event. Can be empty.
            websites: a list of dictionaries containing website urls and wdescriptions. can be empty.
        Return:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()

        # Insert photo into table if it does not exist, then get the photoid.
        photoid = self.insertPhoto(photourl=photourl, cursor=cursor)[0]

        # Build the query to create an event entry.
        query = sql.SQL("insert into {table1} ({insert_fields})"
                        "values (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s) "
                        "returning {pkey1}").format(
            table1=sql.Identifier('events'),
            insert_fields=sql.SQL(',').join([
                sql.Identifier('ecreator'),
                sql.Identifier('roomid'),
                sql.Identifier('etitle'),
                sql.Identifier('edescription'),
                sql.Identifier('estart'),
                sql.Identifier('eend'),
                sql.Identifier('ecreation'),
                sql.Identifier('estatus'),
                sql.Identifier('estatusdate'),
                sql.Identifier('photoid')
            ]),
            pkey1=sql.Identifier('eid'))

        # Try to insert the event into the database, catch if any event is duplicated.
        try:
            cursor.execute(query, (int(ecreator), int(roomid), str(etitle), str(edescription),
                                   str(estart), str(eend), 'active', None, photoid))
            result = cursor.fetchone()
            eid = result[0]
        except errors.UniqueViolation as unique_error:
            return unique_error

        # Once the event is created, tag it with the list of tags provided. Catch any bad tags.
        try:
            for tag in tags:
                TagDAO().tagEvent(eid=eid, tid=tag, cursor=cursor)
        except errors.ForeignKeyViolation as fk_error:
            return fk_error

        # Once tagged, insert the websites, if any, that do not already exist, and relate them to the event.
        if websites is not None:
            try:
                for website in websites:
                    wid = self.insertWebsite(url=website['url'], wdescription=website['wdescription'], cursor=cursor)[0]

                    self.addWebsitesToEvent(eid=eid, wid=wid, cursor=cursor)
            # Do not know if this is the right error to expect.
            except TypeError as e:
                return e

        # Commit changes if no errors occur.
        self.conn.commit()
        return result

    def insertPhoto(self, photourl, cursor):
        """
        Attempt to insert a photo's url into the photos table; Does nothing if the photourl is either None
            or and empty string. DOES NOT COMMIT CHANGES.
        Parameters:
            photourl: a non-empty string or None
            cursor: createEvent method call connection cursor to database.
        Returns:
            Tuple: the photoID of the photo in the Photos table, as an SQL result
        """
        if photourl is not None and photourl != "":
            cursor = cursor
            query = sql.SQL("insert into {table1} "
                            "({insert_field})"
                            "values (%s) on conflict(photourl) "
                            "do update set photourl=%s"
                            "returning {pkey1}").format(
                table1=sql.Identifier('photos'),
                insert_field=sql.Identifier('photourl'),
                pkey1=sql.Identifier('photoid'))
            cursor.execute(query, (str(photourl), str(photourl)))
            result = cursor.fetchone()
        else:
            result = [None, None]
        return result

    def addWebsitesToEvent(self, eid, wid, cursor):
        """
        Relates the websites to the event. DOES NOT COMMIT CHANGES TO
        DB.
        Parameters:
            eid: newly created Event ID.
            wid: website IDs
            cursor: createEvent method call connection cursor to database.
        """
        cursor = cursor
        query = sql.SQL("insert into {table1} "
                        "({insert_fields}) "
                        "values (%s, %s);").format(
            table1=sql.Identifier('eventwebsites'),
            insert_fields=sql.SQL(',').join([
                sql.Identifier('eid'),
                sql.Identifier('wid')
            ]))
        cursor.execute(query, (int(eid), int(wid)))
        return

    def insertWebsite(self, url, wdescription, cursor):
        """Inserts a website into the website table
        Parameters:
            url: the url for the website
            wdescription: a description for the website
            cursor: createEvent method call connection cursor to database.
        Returns:
            wid: website ID
            """
        if url is not None and url != "":
            cursor = cursor
            query = sql.SQL("insert into {table1} "
                            "({insert_fields}) "
                            "values (%s, %s, %s) "
                            "on CONFLICT (url) do update "
                            "set url=%s"
                            "returning wid;").format(
                table1=sql.Identifier('websites'),
                insert_fields=sql.SQL(',').join([
                    sql.Identifier('url'),
                    sql.Identifier('wdescription'),
                    sql.Identifier('isdeleted')
                ]))
            cursor.execute(query, (str(url), wdescription, False, str(url)))
            result = cursor.fetchone()
        else:
            result = [None, None]
        return result

    def getWebsitesByEventID(self, eid):
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "natural join {table2} "
                        "where {pkey1} = %s and {pkey2} = %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('wid'),
                sql.Identifier('url'),
                sql.Identifier('wdescription')
            ]),
            table1=sql.Identifier('eventwebsites'),
            table2=sql.Identifier('websites'),
            pkey1=sql.Identifier('eid'),
            pkey2=sql.Identifier('isdeleted'))
        cursor.execute(query, (int(eid), False))
        result = []
        for row in cursor:
            result.append(row)
        return result




