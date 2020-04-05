from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql, errors


class WebsiteDAO(MasterDAO):

    def getWebsiteByID(self, wid):

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

    def createWebsite(self, url):
        """
        """
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
            cursor.execute(query, (str(url), str(url)))
            self.conn.commit()
            result = cursor.fetchone()
        else:

            result = [None, None]
        return result[0]

    def addWebsite(self, url, cursor):
        """Inserts a website into the website table DOES NOT COMMIT CHANGES TO DB.
        Parameters:
            url: the url for the website
            cursor: createEvent method call connection cursor to database.
        Returns:
            wid: website ID
            """
        if url is not None and url != "" and not url.isspace():
            cursor = cursor
            query = sql.SQL("insert into {table1} "
                            "({insert_fields}) "
                            "values (%s) "
                            "on CONFLICT (url) do update "
                            "set url=%s"
                            "returning wid;").format(
                table1=sql.Identifier('websites'),
                insert_fields=sql.SQL(',').join([
                    sql.Identifier('url')
                ]))
            cursor.execute(query, (str(url), str(url)))

            result = cursor.fetchone()
        else:
            result = [None, None]
        return result

    def addWebsitesToService(self, sid, wid, wdescription, cursor):
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
                        "values (%s, %s, %s, %s );").format(
            table1=sql.Identifier('servicewebsites'),
            insert_fields=sql.SQL(',').join([
                sql.Identifier('sid'),
                sql.Identifier('wid'),
                sql.Identifier('wdescription'),
                sql.Identifier('isdeleted')
            ]))
        cursor.execute(query, (sid, wid, wdescription, False))
        return

    def addWebsitesToEvent(self, eid, wid, wdescription, cursor):
        """
        Relates the websites to the event. DOES NOT COMMIT CHANGES TO
        DB.
        Parameters:
            eid: newly created Event ID.
            wid: website IDs
            wdescription: description of website
            cursor: createEvent method call connection cursor to database.
        """
        cursor = cursor
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
        return

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
                        "values (%s, %s,%s,%s) "
                        "on CONFLICT (sid,wid) do update set isdeleted = %s "
                        "returning wid, sid, isdeleted, wdescription").format(
            table1=sql.Identifier('servicewebsites'),
            insert_fields=sql.SQL(',').join([
                sql.Identifier('sid'),
                sql.Identifier('wid'),
                sql.Identifier('wdescription'),
                sql.Identifier('isdeleted')
            ]))
        cursor.execute(query, (int(sid), int(
            wid), str(wdescription), False, False))

        result = cursor.fetchone()
        self.conn.commit()

        return result

    def removeWebsitesGivenServiceID(self, wid, sid):
        """
        """
        cursor = self.conn.cursor()
        query = sql.SQL("update {table1} set isdeleted = True  "
                        "where ( {pkey1} = %s AND {pkey2} = %s ) "
                        "returning {pkey1} ,sid,isdeleted,wdescription ").format(
            table1=sql.Identifier('servicewebsites'),
            pkey1=sql.Identifier('wid'),
            pkey2=sql.Identifier('sid'))
        try:
            cursor.execute(query, (int(wid), int(sid)))
            result = cursor.fetchone()
            self.conn.commit()
        except errors.ForeignKeyViolation as e:
            result = e
        if result is None:
            return None
        return result[0]
