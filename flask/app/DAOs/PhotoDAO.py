from app.DAOs.MasterDAO import MasterDAO
from app.DAOs.AuditDAO import AuditDAO
from psycopg2 import sql, errors


class PhotoDAO(MasterDAO):

    def insertPhoto(self, photourl, uid, cursor):
        """
        Attempt to insert a photo's url into the photos table; Does nothing if the photourl is either None
            or and empty string. DOES NOT COMMIT CHANGES.
        Parameters:
            photourl: a non-empty string or None
            cursor: createEvent method call connection cursor to database.
        Returns:
            Tuple: the photoID of the photo in the Photos table, as an SQL result
        """
        if photourl is not None and photourl != "" and not photourl.isspace():
            cursor = cursor
            audit = AuditDAO()
            tablename = "photos"
            pkey = "photourl"
            oldValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=photourl, cursor=cursor)

            query = sql.SQL("insert into {table1} "
                            "({insert_field})"
                            "values (%s) on conflict(photourl) "
                            "do update set photourl=%s"
                            "returning {pkey1}").format(
                table1=sql.Identifier('photos'),
                insert_field=sql.Identifier('photourl'),
                pkey1=sql.Identifier('photoid'))
            cursor.execute(query, (str(photourl), str(photourl)))
            result = cursor.fetchone()
            newValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=photourl, cursor=cursor)
            audit.insertAuditEntry(changedTable=tablename, changeType=audit.INSERTVALUE, oldValue=oldValue,
                                   newValue=newValue, uid=uid, cursor=cursor)
        else:
            result = [None, None]
        return result
