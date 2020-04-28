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

    def addPhone(self, pnumber, ptype, cursor):
        """
        Creates a new phone entry
        
        :param pnumber: The phone number in the format of xxx-xxx-xxxx,xxxx in the case of a phone with extension
        :type pnumber: string
        :param ptype: The type of phone can be Fax [F], Land-line [L], Mobile [M] and Extension [E]
        :type ptype: string
        :param cursor: addPhone method call connection cursor to database.
        :type sname: connection cursor
        :return Tuple: SQL result of Query as a tuple.
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
            print(result)
            return result
        else:
            result = [None, None]
    
    def insertPhones(self,phones,sid):
        """
        Adds a list of phones to a service,given the service ID and a list of phone numbers,verifies numbers are valid
        
        :param phones: A list of phone numbers, containing pnumbers and ptypes
        :type phones: array
        :param sid: The Service ID
        :type sid: int
        :cursor cursor: insertPhone method call connection cursor to database.
        :type cursor: connection cursor
        :return Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        
        for row in phones:
                number = phonenumbers.parse(row['pnumber'],"US")
                if((phonenumbers.is_possible_number(number))):
                    phone =self.addPhone(cursor=cursor, pnumber=row['pnumber'], ptype=row['ptype'].upper())      
                    if phone:
                       pid=  self.addPhoneToService(sid=sid,pid=phone[0],cursor=cursor)
                       if pid is None:
                           return jsonify(Error= "Service with sid: "+str(sid)+ " not found"),400
                           
                    else:
                        return jsonify(Error="Phone number error : "+str(number)),400
        self.conn.commit()
        return ({"PNumbers":(phones )})
                                   
    def removePhonesByServiceID(self, sid, phoneid):
        """
        Query Database and mark a phone number and service entry as deleted 
        
        :param phoneid: The phone ID
        :type phoneid: int
        :param sid: The service ID
        :type sid: int
        :return Tuple: SQL result of Query as a tuple.
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
     
        cursor.execute(query, (phoneid, sid))
        result = cursor.fetchone()
        self.conn.commit()
       
        print('Result from Phone remove Query: ' + str(result))

        #print('Result from Phone remove Query: ' + str(result))
        if result == None:
            return None
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

    def addPhoneToService(self, sid, pid, cursor):
        """
        Adds a list of phones to a service,given their respective IDs
        
        :param pid: The ID of a phone number
        :type pid: int
        :param sid: The Service ID
        :type sid: int
        
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
            
            try:
                result = cursor.execute(query, (sid, pid, False))
                result = cursor.fetchone()
                print( result)
                return result
            except:
                return None
        else:
            result = [None, None]
        
        