from app.DAOs.MasterDAO import MasterDAO
from app.DAOs.AuditDAO import AuditDAO
from psycopg2 import sql, errors
from flask import jsonify
import re

def Find(string): 
    # findall() has been used  
    # with valid conditions for urls in string 
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string) 
    return url 
      


class WebsiteDAO(MasterDAO):
    """
    All Methods in this DAO close connections upon proper completion.
    Do not instantiate this class and assign it, as running a method
    call will render it useless afterwards.
    """

    def getWebsiteByID(self, wid):
        """
        Query Database for an Website, given a website ID

        :param wid: The website ID
        :type wid: int
        :return Tuple: SQL result of Query as a tuple.
        """

        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "

                        "where {pkey1} = %s ").format(
            fields=sql.SQL(',').join([
                sql.Identifier('wid'),
                sql.Identifier('url')

            ]),
            table1=sql.Identifier('websites'),

            pkey1=sql.Identifier('wid'))

        cursor.execute(query, (int(wid),))
        result = cursor.fetchone()
        return result

    def getWebsitesByEventID(self, eid):
        """
        Query Database for an Website, given a event ID

        :param eid: The event ID
        :type eid: int
        :return Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "natural join {table2} "
                        "where {pkey1} = %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('wid'),
                sql.Identifier('url'),
                sql.Identifier('wdescription')
            ]),
            table1=sql.Identifier('eventwebsites'),
            table2=sql.Identifier('websites'),
            pkey1=sql.Identifier('eid'))
        cursor.execute(query, (int(eid),))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getWebsitesByServiceID(self, sid):
        """
        Query Database for an Website, given a service ID

        :param sid: The service ID
        :type sid: int
        :return Tuple: SQL result of Query as a tuple.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "natural join {table2} "
                        "where {pkey1} = %s and {pkey2} = %s and isdeleted = false ").format(
            fields=sql.SQL(',').join([
                sql.Identifier('wid'),
                sql.Identifier('url'),
                sql.Identifier('wdescription'),
                sql.Identifier('isdeleted')
            ]),
            table1=sql.Identifier('servicewebsites'),
            table2=sql.Identifier('websites'),
            pkey1=sql.Identifier('sid'),
            pkey2=sql.Identifier('isdeleted'))
        cursor.execute(query, (int(sid), False))
        self.conn.commit()
        result = []
        for row in cursor:
            result.append(row)
        return result

    def createWebsite(self, url,uid):
        """
        Create a new entry for service websites

        :param url: The website link
        :type url: string
        :param uid: The user id of the route caller 
        :type uid: int
        :return Tuple: SQL result of Query as a tuple.
        """      
        try:
            if url is not None and url != "":
                cursor = self.conn.cursor()
                query = sql.SQL("insert into {table1} "
                            "({insert_fields}) "
                            "values (%s) "
                            "on CONFLICT (url) do update "
                            "set url=%s "
                            "returning wid ").format(
                table1=sql.Identifier('websites'),
                insert_fields=sql.SQL(',').join([
                    sql.Identifier('url'),

                ]))
                cursor.execute(query, (url, url))
                result = cursor.fetchone()
                return result    
            else:
                result = [None, None]
        except:
           result = [None, None]
           return result 

    def addWebsite(self, url, cursor,uid):
        """
        Create a new entry for a website

        :param url: The website link
        :type url: string
        :param uid: The user id of the route caller 
        :type uid: int
        :param cursor: addWebsite method call connection cursor to database.
        :type sname: connection cursor
        :return Tuple: SQL result of Query as a tuple.
        """ 
        temp =url
        url = Find(url)
        cursor = cursor    
        if (url is not None )and (url != "") and len(url)> 0:
                query = sql.SQL("insert into {table1} "
                            "({insert_fields}) "
                            "values (%s) "
                            "on CONFLICT (url) do update "
                            "set url=%s "
                            "returning wid, url").format(
                    table1=sql.Identifier('websites'),
                    insert_fields=sql.SQL(',').join([
                        sql.Identifier('url')
                                                    ]))
                cursor.execute(query, (temp,temp ))
                result = cursor.fetchone()
                return result
        else:
            raise ValueError("URL not valid: "+str(temp))
              
    def addWebsitesToService(self, sid, wid, wdescription, cursor):
        """
        Create a new entry for a website services table

        :param sid: The Service ID
        :type sid: int
        :param wid: The website ID
        :type wid: int
        :param wdescription: Description for  the website 
        :type wdescription: string
        :param cursor: Method call connection cursor to database.
        :type sname: connection cursor
        :return Tuple: SQL result of Query as a tuple.
        """ 
        
        cursor =cursor
        
        query = sql.SQL("insert into {table1} "
                        "({insert_fields}) "
                        "values (%s, %s,%s,%s) "
                        "on CONFLICT (wid,sid) do update set isdeleted = %s "
                        "returning wid, sid, isdeleted, wdescription").format(
        table1=sql.Identifier('servicewebsites'),
        insert_fields=sql.SQL(',').join([
                sql.Identifier('sid'),
                sql.Identifier('wid'),
                sql.Identifier('wdescription'),
                sql.Identifier('isdeleted')
            ]))
        
        try:
            cursor.execute(query, (int(sid), str(wid), str(wdescription), False, False))
            result = cursor.fetchone()
            return result
        except:
            return None

    def addWebsitesToEvent(self, eid, wid, wdescription, cursor, uid):
        """
        Create a new entry for a website events table

        :param eid: The Event ID
        :type eid: int
        :param wid: The website ID
        :type wid: int
        :param wdescription: Description for  the website 
        :type wdescription: string
        :param uid: The user id of the route caller 
        :type uid: int
        :param cursor: Method call connection cursor to database.
        :type sname: connection cursor
        :return Tuple: SQL result of Query as a tuple.
        """
        cursor = cursor
        audit = AuditDAO()
        tablename = 'eventwebsites'
        pkeys = ["eid", "wid"]
        oldValue = audit.getTableValueByPkeyPair(table=tablename, pkeyname1=pkeys[0], pkeyname2=pkeys[1],
                                                 pkeyval1=eid, pkeyval2=wid, cursor=cursor)
        query = sql.SQL("insert into {table1} "
                        "({insert_fields}) "
                        "values (%s, %s, %s);").format(
            table1=sql.Identifier('eventwebsites'),
            insert_fields=sql.SQL(',').join([
                sql.Identifier('eid'),
                sql.Identifier('wid'),
                sql.Identifier('wdescription')
            ]))
        cursor.execute(query, (int(eid), int(wid), wdescription))
        newValue = audit.getTableValueByPkeyPair(table=tablename, pkeyname1=pkeys[0], pkeyname2=pkeys[1],
                                                 pkeyval1=eid, pkeyval2=wid, cursor=cursor)
        audit.insertAuditEntry(changedTable=tablename, changeType=audit.INSERTVALUE, oldValue=oldValue,
                               newValue=newValue, uid=uid, cursor=cursor)
        return

    def insertWebsiteToService(self, sites,sid):
        """
        Create a new entry for a website services table

        :param sid: The Service ID
        :type sid: int
        :param sites: List of wids and wdescriptions\
        :type sites: array
        :param cursor: Method call connection cursor to database.
        :type cursor: connection cursor
        :return Tuple: SQL result of Query as a tuple.
        """ 
        websites =[]
        cursor = self.conn.cursor()
        
        for site in sites:
            website =self.addWebsite(cursor=cursor,url=site['url'])
            if website:
                websites.append({"url":website[1],"wid":website[0],"wdescription":site['wdescription']})
            else:
                return jsonify(Error= "Error creating website "+str(site['url']))
        
        
        
        for site in websites:
            result= self.addWebsitesToService(cursor=cursor,sid=sid,wid=site['wid'],wdescription=site['wdescription'])
            if result is None:
                return jsonify(Error= "Error assigning website to sid: "+str(sid)),400
            
       
        self.conn.commit()

        return {"Websites":websites}
        
    def removeWebsitesGivenServiceID(self, wid, sid,uid):
        """
        Remove an entry from a website services table

        :param sid: The Service ID
        :type sid: int
        :param wid: The website ID
        :type wid: int
        :param uid: The user id of the route caller 
        :type uid: int
        :return Tuple: SQL result of Query as a tuple.
        """ 
        cursor = self.conn.cursor()
        audit = AuditDAO()
        tablename = 'servicewebsites'
        pkeys = ["sid", "wid"]
        oldValue = audit.getTableValueByPkeyPair(table=tablename, pkeyname1=pkeys[0], pkeyname2=pkeys[1],
                                                 pkeyval1=sid, pkeyval2=wid, cursor=cursor)
        query = sql.SQL("update {table1} set isdeleted = True  "
                        "where ( {pkey1} = %s AND {pkey2} = %s ) "
                        "returning {pkey1} ,sid,isdeleted,wdescription ").format(
            table1=sql.Identifier('servicewebsites'),
            pkey1=sql.Identifier('wid'),
            pkey2=sql.Identifier('sid'))
        try:
            cursor.execute(query, (int(wid), int(sid)))
            result = cursor.fetchone()
            newValue = audit.getTableValueByPkeyPair(table=tablename, pkeyname1=pkeys[0], pkeyname2=pkeys[1],
                                                     pkeyval1=sid, pkeyval2=wid, cursor=cursor)
            if oldValue and newValue:
                audit.insertAuditEntry(changedTable=tablename, changeType=audit.UPDATEVALUE, oldValue=oldValue,
                                       newValue=newValue, uid=uid, cursor=cursor)
            self.conn.commit()
        except errors.ForeignKeyViolation as e:
            result = e
        if result is None:
            return None
        return result[0]
