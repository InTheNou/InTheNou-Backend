from app.DAOs.MasterDAO import MasterDAO
from app.DAOs.PhotoDAO import PhotoDAO
from app.DAOs.TagDAO import TagDAO
from app.DAOs.WebsiteDAO import WebsiteDAO
from psycopg2 import sql, errors

# Ammount to change when increasing/decreasing user tags.
STANDARD_CHANGE = 5
FOLLOWING_STRING = 'following'
DISMISSED_STRING = 'dismissed'
UNFOLLOWED_STRING = 'unfollowed'
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

        # Get existing user event interaction.
        query = sql.SQL("select itype from eventuserinteractions "
                        "where eid=%s and uid=%s;")
        cursor.execute(query, (int(eid), int(uid)))
        current_itype = cursor.fetchone()

        # Determine what amount to add/subtract from tags.
        if current_itype is None:
            if itype == FOLLOWING_STRING:
                weight_change = STANDARD_CHANGE
            else:
                weight_change = -STANDARD_CHANGE
        else:
            if itype == DISMISSED_STRING:
                if current_itype[0] == FOLLOWING_STRING:
                    weight_change = -2 * STANDARD_CHANGE
                else:
                    weight_change = -STANDARD_CHANGE
            elif itype == UNFOLLOWED_STRING:
                weight_change = -STANDARD_CHANGE
            else:
                weight_change = STANDARD_CHANGE

        # Get a list of the event's tags and whatever weights the user has.
        tag_weights = TagDAO().getCoreUserTagsFromEventID(uid=uid, eid=eid,
                                                          cursor=cursor)
        # Determine how to set the usertag weight.
        try:
            for t_w in tag_weights:
                tid = t_w[0]
                new_weight=-1

                # The user has a weight entry for the given tag:
                if t_w[1] is not None:
                    current_weight = t_w[1]

                    if (weight_change > 0) and (current_weight+weight_change >= 200):
                        new_weight = 200  # If adding weight goes over limit, set to limit.
                    elif (weight_change < 0) and (current_weight+weight_change <= 0):
                        new_weight = 0  # If subtracting weight goes below limit, set to lower limit.
                    else:
                        new_weight = current_weight + weight_change  # Else, add to weight

                # The user does not have a weight entry for the given tag:
                else:
                    if weight_change > 0:
                        new_weight = weight_change  # If the weight is to be added, create an entry with weight.
                    else:
                        pass  # Entry would be negative, so pass.
                if new_weight >= 0:
                    # If the new weight was set above, run the query to set user tag.
                    TagDAO().setUserTag(uid=uid, tid=tid, weight=new_weight, cursor=cursor)
        except errors.ForeignKeyViolation as fke:
            return fke

        # if you get here with no errors, update the interaction and finish.
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
        photoid = PhotoDAO().insertPhoto(photourl=photourl, cursor=cursor)[0]

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
                    wid = WebsiteDAO().insertWebsite(url=website['url'], wdescription=website['wdescription'], cursor=cursor)[0]

                    WebsiteDAO().addWebsitesToEvent(eid=eid, wid=wid, cursor=cursor)
            # Do not know if this is the right error to expect.
            except TypeError as e:
                return e

        # Commit changes if no errors occur.
        self.conn.commit()
        return result
