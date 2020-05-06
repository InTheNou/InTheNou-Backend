from app.DAOs.MasterDAO import MasterDAO
from app.DAOs.AuditDAO import AuditDAO
from psycopg2 import sql, errors
import phonenumbers
from flask import jsonify


class PhoneDAO(MasterDAO):
    """
    All Methods in this DAO close connections upon proper completion.
    Do not instantiate this class and assign it, as running a method
    call will render it useless afterwards.
    """

    def getPhoneByID(self, phoneid):
        """
        Query Database for an Phone number, given a phone ID

        :param phoneid: The phone ID
        :type phoneid: int
        :return Tuple: SQL result of Query as a tuple.
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

    def addPhone(self, pnumber, ptype, cursor, uid):
        """
        Creates a new phone entry
        
        :param pnumber: The phone number in the format of xxx-xxx-xxxx,xxxx in the case of a phone with extension
        :type pnumber: string
        :param ptype: The type of phone can be Fax [F], Land-line [L], Mobile [M] and Extension [E]
        :type ptype: string
        :param cursor: addPhone method call connection cursor to database.
        :type cursor: connection cursor
        :param uid: User ID
        :type uid: int
        :return Tuple: SQL result of Query as a tuple.
        """
        
        if pnumber is not None and pnumber != "":
            if cursor is None:
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
                            "on CONFLICT (pnumber, ptype) do update "
                            "set pnumber=%s , ptype =%s "
                            "returning phoneid, ptype;").format(
                table1=sql.Identifier('phones'),
                insert_fields=sql.SQL(',').join([
                    sql.Identifier('pnumber'),
                    sql.Identifier('ptype')

                ]))
            cursor.execute(query, (pnumber, ptype[0], pnumber,ptype[0]))
            result = cursor.fetchone()
            newValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=pnumber, cursor=cursor)
            audit.insertAuditEntry(changedTable=tablename, changeType=audit.INSERTVALUE, oldValue=oldValue,
                                   newValue=newValue, uid=uid, cursor=cursor)
        else:
            result = [None, None]
        return result

    def insertPhones(self, phones, sid, uid):
        """
        Adds a list of phones to a service,given the service ID and a list of phone
        numbers,verifies numbers are valid.
        Uses :func:`~app.DAOs.PhoneDAO.PhoneDAO.addPhone` &
        :func:`~app.DAOs.PhoneDAO.PhoneDAO.addPhoneToService`
        
        :param phones: A list of phone numbers, containing pnumbers and ptypes
        :type phones: array
        :param sid: The Service ID
        :type sid: int
        :param uid: User ID
        :type uid: int
        :return Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        
        for row in phones:
            number = phonenumbers.parse(row['pnumber'], "US")
            if phonenumbers.is_possible_number(number):
                phone = self.addPhone(cursor=cursor, pnumber=row['pnumber'], ptype=(row['ptype'].upper()), uid=uid)
                if phone:
                    pid = self.addPhoneToService(sid=sid, pid=phone[0], cursor=cursor, uid=uid)
                    if pid is None:
                        return jsonify(Error="Service with sid: " + str(sid) + " not found"), 400
                    else:
                        row['phoneid']=pid[0]
                else:
                    return jsonify(Error="Phone number error : "+str(number)), 400
        self.conn.commit()
        return {"numbers": phones}
                                   
    def removePhonesGivenServiceID(self,phones,sid,uid):
        phoneIDs = []
        phoneInfo=[]
        
        cursor = self.conn.cursor()
        print("Starting "+ str(phones))
        
        for phone in phones:
            if phone['phoneid'] != "":
                   
                    ID = self.removePhonesByServiceID(cursor=cursor,sid=sid, phoneid=phone['phoneid'], uid=uid)
                    print("This "+str(ID))
                    if isinstance(ID,tuple):
                        return jsonify(Error="Phone not asociated with service "+str(phone['phoneid'])),404
                    
                    else:
                        phoneIDs.append(ID)
                        
            else:       
                return jsonify(Error="Phone number ID not associated with Service-> sid: "
                                     + str(sid) + ' phoneid: ' + str(phone['phoneid'])),404
         
        self.conn.commit()
   
        return phoneIDs
    
    def removePhonesByServiceID(self,cursor, sid, phoneid, uid):
        """
        Query Database and mark a phone number and service entry as deleted.
        
        :param phoneid: The phone ID
        :type phoneid: int
        :param sid: The service ID
        :type sid: int
        :param uid: User ID
        :type uid: int
        :return Tuple: SQL result of Query as a tuple.
        """
        #print('Number ID from Phone remove Query: '+phoneid)
        cursor = cursor

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
     
        cursor.execute(query, (phoneid, sid))
        result = cursor.fetchone()
        # If result is None, skip auditing.
        if result:
            newValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=phoneid, cursor=cursor)
            audit.insertAuditEntry(changedTable=tablename, changeType=audit.UPDATEVALUE, oldValue=oldValue,
                                   newValue=newValue, uid=uid, cursor=cursor)
        
        if result is None:
            return jsonify(Error= "The service:"+str(sid)+" was not asociated with the phoneid: "+str(phoneid)),404
        else:
            return result[0]

    def getPhonesByServiceID(self, sid):
        """
        Gets a list of phones, given a service ID 
        
        :param sid: The Service ID
        :type sid: int
        :return Tuple: SQL result of Query as a tuple.
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

    def addPhoneToService(self, sid, pid, cursor, uid):
        """
        Adds a list of phones to a service,given their respective IDs.
        
        :param pid: The ID of a phone number
        :type pid: int
        :param sid: The Service ID
        :type sid: int
        :param cursor: addPhone method call connection cursor to database.
        :type cursor: connection cursor
        :param uid: User ID
        :type uid: int
        :return Tuple: SQL result of Query as a tuple.
        """
        if pid is not None and pid != "":
            if cursor is None:
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
            
            try:
                cursor.execute(query, (sid, pid, False))
                result = cursor.fetchone()
                newValue = audit.getTableValueByPkeyPair(table=tablename, pkeyname1=pkeys[0], pkeyname2=pkeys[1],
                                                         pkeyval1=sid, pkeyval2=pid, cursor=cursor)
                audit.insertAuditEntry(changedTable=tablename, changeType=audit.INSERTVALUE, oldValue=oldValue,
                                       newValue=newValue, uid=uid, cursor=cursor)
            except:
                return None
        else:
            result = [None, None]
        return result
