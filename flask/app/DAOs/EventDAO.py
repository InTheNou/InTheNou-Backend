from app.DAOs.MasterDAO import MasterDAO


class EventDAO(MasterDAO):

    def getEventByID(self, eid):
        cursor = self.conn.cursor()
        query = "select * from users where uid=2;"
        cursor.execute(query)
        result = cursor.fetchone()
        return str(result)