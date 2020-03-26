from app.DAOs.MasterDAO import MasterDAO
from psycopg2 import sql, errors


class PhotoDAO(MasterDAO):

    def insertPhoto(self, photourl, cursor):
        """
        Attempt to insert a photo's url into the photos table; Does nothing if the photourl is either None
            or and empty string. DOES NOT COMMIT CHANGES.
        Parameters:
            photourl: a non-empty string or None
            cursor: createEvent method call connection cursor to database.
        Returns:
            Tuple: the photoID of the photo in the Photos table, as an SQL result
        """
        if photourl is not None and photourl != "":
            cursor = cursor
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
        else:
            result = [None, None]
        return result
