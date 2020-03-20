from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.EventDAO import EventDAO

class EventHandler():

    def testHandler(self, test_int):
        dao = EventDAO()
        return dao.getEventByID(test_int)
        # return jsonify({"response" : "you sent me: " + str(test_int)})