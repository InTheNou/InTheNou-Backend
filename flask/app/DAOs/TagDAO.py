from app.DAOs.MasterDAO import MasterDAO
from app.DAOs.AuditDAO import AuditDAO
from psycopg2 import sql, errors


class TagDAO(MasterDAO):

    def createTag(self, tname, uid):
        """
        Create a new Tag in the system
        Parameters:
           :param  tname: The name of the new tag to be created
           :param  uid: The tag creator User ID
           
           :return  Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()

        audit = AuditDAO()
        tablename = "tags"
        pkey = "tname"
        oldValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=tname, cursor=cursor)
        # Build the query to create an event entry.
        query = sql.SQL("insert into {table1} (tname)  "
                        "VALUES (  %s ) "
                        "ON CONFLICT (tname) do update set tname = %s "
                        "returning tid, tname ").format(
            table1=sql.Identifier('tags'))
        cursor.execute(query, (str(tname), str(tname)))
        result = cursor.fetchone()
        newValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=tname, cursor=cursor)
        audit.insertAuditEntry(changedTable=tablename, changeType=audit.INSERTVALUE, oldValue=oldValue,
                               newValue=newValue, uid=uid, cursor=cursor)
        self.conn.commit()
        return result

    def editTagName(self, tid, tname, uid):
        """
        Edit the name of a Tag in the system,given it's ID
        Parameters:
           :param  tname: The new name of the tag to be edited
           :param tid: The Tag ID 
           :param  uid: The tag creator User ID
           
           :return  Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        # Build the query to create an event entry.\
        try:
            audit = AuditDAO()
            tablename = "tags"
            pkey = "tid"
            oldValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=tid, cursor=cursor)

            query = sql.SQL("update  {table1} SET   "
                            "tname =  %s  "
                            "WHERE tid = %s "
                            "returning tid, tname ").format(
                table1=sql.Identifier('tags'))
            cursor.execute(query, (str(tname), int(tid)))
            result = cursor.fetchone()
            newValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=tid, cursor=cursor)
            audit.insertAuditEntry(changedTable=tablename, changeType=audit.UPDATEVALUE, oldValue=oldValue,
                                   newValue=newValue, uid=uid, cursor=cursor)
            self.conn.commit()
            return result

        except errors.UniqueViolation as badkey:
            return badkey

    def getTagByID(self, tid):
        """
         Query Database for an Tag's information by its tid.
        Parameters:
            :param tid: tag ID
        
            :return Tuple: SQL result of Query as a tuple.
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
            :param eid: event ID
       
            :return Tuple: SQL result of Query as a tuple.
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
            :param uid: User ID
        
           :return  Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "natural join {table2} "
                        "natural join {table3} "
                        "where {pkey}= %s and tagweight > 0;").format(
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

    def tagEvent(self, eid, tid, cursor):
        """
        Tag the specified event with the specified tag. DOES NOT COMMIT CHANGES TO
        DB.
        Parameters:
           :param  eid: newly created Event ID.
           :param  tid: tag ID
           :param  cursor: createEvent method call connection cursor to database.
           :return  Tuple: SQL result of Query as a tuple.
        """
        cursor = cursor
        # Currently not auditing this method, since creating an event stores info on who and when.
        query = sql.SQL("insert into {table1} "
                        "({insert_fields}) "
                        "values (%s, %s);").format(
            table1=sql.Identifier('eventtags'),
            insert_fields=sql.SQL(',').join([
                sql.Identifier('eid'),
                sql.Identifier('tid')
            ]))
        cursor.execute(query, (int(eid), int(tid)))

#TODO: METHOD NOT CURRENTLY AUDITING.
    def setUserTag(self, uid, tid, weight, cursor):
        """
        Associate a user account with a specified tag 
        Parameters:
           :param  uid: The user ID
           :param  tid: tag ID
           :param weight: The importance of a tag to a specified user
           :param  cursor: createEvent method call connection cursor to database.
           :return  Tuple: SQL result of Query as a tuple.
        """
        cursor = cursor
        query = sql.SQL("insert into {table}({fields}) "
                        "values (%s, %s, %s) "
                        "on Conflict(uid,tid) "
                        "do update "
                        "set tagweight=%s "
                        "returning {fields};").format(
            fields=sql.SQL(',').join([
                sql.Identifier('uid'),
                sql.Identifier('tid'),
                sql.Identifier('tagweight')
            ]),
            table=sql.Identifier('usertags'))
        cursor.execute(query, (int(uid), int(tid), int(weight), int(weight)))
        result = cursor.fetchone()
        return result

#TODO: METHOD NOT CURRENTLY AUDITING
    def batchSetUserTags(self, uid, tags, weight):
        """
       Assign a list of tags to a user
        Parameters:
           :param tags: list of the tag IDs to associate with the user
           :param  uid: The tag creator User ID
           :param weight: The importance of a tag to a specified user
           :return  Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        result = []
        try:
            for tid in tags:
                query = sql.SQL("insert into {table}({fields}) "
                                "values (%s, %s, %s) "
                                "on Conflict(uid,tid) "
                                "do update "
                                "set tagweight=%s "
                                "returning {fields};").format(
                    fields=sql.SQL(',').join([
                        sql.Identifier('uid'),
                        sql.Identifier('tid'),
                        sql.Identifier('tagweight')
                    ]),
                    table=sql.Identifier('usertags'))
                cursor.execute(query, (int(uid), int(
                    tid), int(weight), int(weight)))
                result.append(cursor.fetchone())
            self.conn.commit()
        except errors.ForeignKeyViolation as badkey:
            return badkey
        return result
#TODO:FINISH DOCUMENTATION ON THIS METHOD
    def getCoreUserTagsFromEventID(self, uid, eid, cursor):
        """
    
        """
        cursor = cursor
        query = sql.SQL("select et.tid, cuser.tagweight from "
                        "eventtags as et "
                        "left outer join "
                        "(select * from usertags where uid = %s) as cuser "
                        "on et.tid = cuser.tid "
                        "where et.eid = %s")
        cursor.execute(query, (str(uid), int(eid)))
        result = []
        for row in cursor:
            result.append(row)
        return result
