from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql, errors


class WebsiteDAO(MasterDAO):

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

    def insertWebsite(self, url, cursor):
        """Inserts a website into the website table DOES NOT COMMIT CHANGES TO DB.
        Parameters:
            url: the url for the website
            cursor: createEvent method call connection cursor to database.
        Returns:
            wid: website ID
            """
        if url is not None and url != "":
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
