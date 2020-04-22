from app.DAOs.MasterDAO import MasterDAO
from app.DAOs.AuditDAO import AuditDAO
from psycopg2 import sql, errors


class PhoneDAO(MasterDAO):

    def getPhoneByID(self, phoneid):
        """
        Return a phone number given a phone ID 
        parameters:
        phoneid: the ID for the phone number to look for 
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "

                        "where {pkey1} = %s ").format(
            fields=sql.SQL(',').join([
                sql.Identifier('phoneid'),
                sql.Identifier('pnumber'),
                sql.Identifier('ptype')
            ]),
            table1=sql.Identifier('phones'),

            pkey1=sql.Identifier('phoneid'))

        cursor.execute(query, (int(phoneid),))
        
        result = cursor.fetchone()

        return result

    def insertPhone(self, pnumber, ptype, cursor, uid):
        """Inserts a phone number into the database 
        Parameters:
            pnumber: number of the entry
            ptype: The type of phone i.e. fax, cellphone etc.
            ideleted: indicates if value is active in the database
        Returns:
            pid: phone ID
        """

        if pnumber is not None and pnumber != "":
            if cursor == None:
                cursor = self.conn.cursor()
            else:
                cursor = cursor

            audit = AuditDAO()
            tablename = "phones"
            pkey = "pnumber"
            oldValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=pnumber, cursor=cursor)

            query = sql.SQL("insert into {table1} "
                            "({insert_fields}) "
                            "values (%s, %s) "
                            "on CONFLICT (pnumber) do update "
                            "set pnumber=%s"
                            "returning phoneid;").format(
                table1=sql.Identifier('phones'),
                insert_fields=sql.SQL(',').join([
                    sql.Identifier('pnumber'),
                    sql.Identifier('ptype')

                ]))
            cursor.execute(query, (pnumber, ptype[0], pnumber))
            result = cursor.fetchone()

            newValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=pnumber, cursor=cursor)
            audit.insertAuditEntry(changedTable=tablename, changeType=audit.INSERTVALUE, oldValue=oldValue,
                                   newValue=newValue, uid=uid, cursor=cursor)
            self.conn.commit()
        else:
            result = [None, None]
        return result

    def removePhonesByServiceID(self, sid, phoneid, uid):
        """
        Remove a phone number from a service, given a service ID and a phone ID 
        Parameters 
        sid: The unique ID of a service 
        phoneid: The ID for the phone to eliminate from the database 
        """
        #print('Number ID from Phone remove Query: '+phoneid)
        cursor = self.conn.cursor()

        audit = AuditDAO()
        tablename = "servicephones"
        pkey = "phoneid"
        oldValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=phoneid, cursor=cursor)

        query = sql.SQL("update {table1} set isdeleted = True  "
                        "where ( {pkey1} = %s AND {pkey2} = %s  ) "
                        "returning {pkey1} ").format(
            table1=sql.Identifier('servicephones'),
            pkey1=sql.Identifier('phoneid'),
            pkey2=sql.Identifier('sid'))
        try:
            cursor.execute(query, (int(phoneid), int(sid)))
            result = cursor.fetchone()
            newValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=phoneid, cursor=cursor)
            audit.insertAuditEntry(changedTable=tablename, changeType=audit.UPDATEVALUE, oldValue=oldValue,
                                   newValue=newValue, uid=uid, cursor=cursor)
            self.conn.commit()
        except errors.ForeignKeyViolation as e:
            result = e
            print('Result from Phone remove Query: ' + str(result))

        #print('Result from Phone remove Query: ' + str(result))
        if result == None:
            return None
        else:
            return result[0]

    def getPhonesByServiceID(self, sid):
        """
         Query Database for all the phone entries belonging
            to a Service, given the Service's ID.
        Parameters:
            sid: Service ID
        Returns:
            Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "natural join {table2} "
                        "where {pkey}= %s and isdeleted = false ").format(
            fields=sql.SQL(',').join([
                sql.Identifier('phoneid'),
                sql.Identifier('pnumber'),
                sql.Identifier('ptype'),
                sql.Identifier('isdeleted'),
            ]),
            table1=sql.Identifier('servicephones'),
            table2=sql.Identifier('phones'),
            pkey=sql.Identifier('sid'))
        cursor.execute(query, (int(sid),))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def addPhoneToService(self, sid, pid, uid, cursor):
        """
        Relates the phone number to the service. 
        Parameters:
            sid: newly created Service ID.
            id: phone IDs
            cursor: createService method call connection cursor to database.
        """
        if pid is not None and pid != "":
            if cursor == None:
                cursor = self.conn.cursor()
            cursor = cursor

            audit = AuditDAO()
            tablename = 'servicephones'
            pkeys = ["sid", "phoneid"]
            oldValue = audit.getTableValueByPkeyPair(table=tablename, pkeyname1=pkeys[0], pkeyname2=pkeys[1],
                                                     pkeyval1=sid, pkeyval2=pid, cursor=cursor)

            query = sql.SQL("insert into {table1} "
                            "({insert_fields}) "
                            "values (%s, %s,%s) "
                            " on CONFLICT (sid, phoneid) do update set isdeleted= false  "
                            "returning phoneid  ").format(
                table1=sql.Identifier('servicephones'),
                insert_fields=sql.SQL(',').join([
                    sql.Identifier('sid'),
                    sql.Identifier('phoneid'),
                    sql.Identifier('isdeleted')
                ]))
            cursor.execute(query, (sid, pid, False))
            result = cursor.fetchone()

            newValue = audit.getTableValueByPkeyPair(table=tablename, pkeyname1=pkeys[0], pkeyname2=pkeys[1],
                                                     pkeyval1=sid, pkeyval2=pid, cursor=cursor)
            audit.insertAuditEntry(changedTable=tablename, changeType=audit.INSERTVALUE, oldValue=oldValue,
                                   newValue=newValue, uid=uid, cursor=cursor)
            self.conn.commit()
        else:
            result = [None, None]
        return result
