from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql, errors


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

    def getTagsByEventID(self, eid):
        """
         Query Database for all the tags belonging
            to an event, given the event's ID.
        Parameters:
            eid: event ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "natural join {table2} "
                        "natural join {table3} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('tid'),
                sql.Identifier('tname')
            ]),
            table1=sql.Identifier('events'),
            table2=sql.Identifier('eventtags'),
            table3=sql.Identifier('tags'),
            pkey=sql.Identifier('eid'))
        cursor.execute(query, (int(eid),))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllTags(self):
        """
         Query Database all tag entries.
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table};").format(
            fields=sql.SQL(',').join([
                sql.Identifier('tid'),
                sql.Identifier('tname')
            ]),
            table=sql.Identifier('tags'))
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getTagsByUserID(self, uid):
        """
         Query Database for all the tags belonging
            to a User, given the user's ID.
        Parameters:
            uid: User ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "natural join {table2} "
                        "natural join {table3} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('tid'),
                sql.Identifier('tname'),
                sql.Identifier('tagweight')
            ]),
            table1=sql.Identifier('users'),
            table2=sql.Identifier('usertags'),
            table3=sql.Identifier('tags'),
            pkey=sql.Identifier('uid'))
        cursor.execute(query, (int(uid),))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def tagEvent(self, eid, tid):
        """
        Tag the specified event with the specified tag. DOES NOT COMMIT CHANGES TO
        DB.
        Parameters:
            eid: newly created Event ID.
            tid: tag ID
        """
        cursor = self.conn.cursor()
        result = 'successfully tagged event.'
        try:
            query = sql.SQL("insert into {table1} "
                            "({insert_fields}) "
                            "values (%s, %s);").format(
                table1=sql.Identifier('eventtags'),
                insert_fields=sql.SQL(',').join([
                    sql.Identifier('eid'),
                    sql.Identifier('tid')
                ]))
            cursor.execute(query, (int(eid), int(tid)))
            # TODO: FIGURe out how to commit at end of inserts.
            self.conn.commit()
        except errors.ForeignKeyViolation as e:
            result = e
        return result

