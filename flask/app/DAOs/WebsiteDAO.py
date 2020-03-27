from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql, errors


class WebsiteDAO(MasterDAO):
    
    def removeServiceWebsite(self,wid,sid):
        """
        """
        cursor = self.conn.cursor()
        query = sql.SQL("delete from {table1} "
                        "where {pkey1}= %s AND {pkey2}=%s "
                        "returning {pkey1} ").format(
            table1=sql.Identifier('servicewebsites'),
            pkey1=sql.Identifier('wid'),
            pkey2=sql.Identifier('sid'))
        try:
            cursor.execute(query, (int(wid), int(sid)))
            result = cursor.fetchone()
            self.conn.commit()
        except errors.ForeignKeyViolation as e:
            result = e
        return result

    
    
    
    def getWebsitesByServiceID(self, sid):
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "natural join {table2} "
                        "where {pkey1} = %s and {pkey2} = %s;").format(
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
        result = []
        for row in cursor:
            result.append(row)
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
    
    
    def createWebsite(self,url):
        """
        """
        
        if url is not None and url != "":
            cursor = self.conn.cursor()
            query = sql.SQL("insert into {table1} "
                            "({insert_fields}) "
                            "values (%s) "
                            "on CONFLICT (url) do update "
                            "set url=%s"
                            "returning wid;").format(
                table1=sql.Identifier('websites'),
                insert_fields=sql.SQL(',').join([
                    sql.Identifier('url'),
                    
                ]))
            cursor.execute(query, (str(url), str(url)))
            result = cursor.fetchone()
        else:
            result = [None, None]
        return result
    
    
    def insertWebsite(self, url, wdescription, cursor):
        """Inserts a website into the website table DOES NOT COMMIT CHANGES TO DB.
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
    
    
    def insertWebsiteToService(self, sid, wid, wdescription):
        """
        Relates the websites to the event. DOES NOT COMMIT CHANGES TO
        DB.
        Parameters:
            sid: newly created Service ID.
            wid: website IDs
            cursor: createService method call connection cursor to database.
        """
        cursor = self.conn.cursor()
        query = sql.SQL("insert into {table1} "
                        "({insert_fields}) "
                        "values (%s, %s,%s,%s);").format(
            table1=sql.Identifier('servicewebsites'),
            insert_fields=sql.SQL(',').join([
                sql.Identifier('sid'),
                sql.Identifier('wid'),
                sql.Identifier('wdescription'),
                sql.Identifier('isdeleted')
            ]))
        cursor.execute(query, (sid, wid,wdescription,False))
        return
    
    
    def addWebsitesToService(self, sid, wid, cursor):
        """
        Relates the websites to the event. DOES NOT COMMIT CHANGES TO
        DB.
        Parameters:
            sid: newly created Service ID.
            wid: website IDs
            cursor: createService method call connection cursor to database.
        """
        cursor = cursor
        query = sql.SQL("insert into {table1} "
                        "({insert_fields}) "
                        "values (%s, %s);").format(
            table1=sql.Identifier('servicewebsites'),
            insert_fields=sql.SQL(',').join([
                sql.Identifier('sid'),
                sql.Identifier('wid')
            ]))
        cursor.execute(query, (sid, wid))
        return
   
   
   
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


    def getWebsiteByID(self,wid):

        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        
                        "where {pkey1} = %s ").format(
            fields=sql.SQL(',').join([
                sql.Identifier('wid'),
              
            ]),
            table1=sql.Identifier('websites'),
            
            pkey1=sql.Identifier('wid'))
            
        cursor.execute(query, (int(wid),))
        result = cursor.fetchone()
        return result




        