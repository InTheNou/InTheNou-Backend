from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.EventDAO import EventDAO

class EventHandler():

    def _buildEventResponse(self, eventTuple):
        response = {}
        response['ecreator'] = eventTuple[0]
        response['roomid'] = eventTuple[1]
        response['etitle'] = eventTuple[2]
        response['edescription'] = eventTuple[3]
        response['estart'] = eventTuple[4]
        response['eend'] = eventTuple[5]
        response['photoid'] = eventTuple[6]
        return response

    def getEventByID(self, eid):
        dao = EventDAO()
        event = dao.getEventByID(eid)
        if not event:
            return jsonify(Error='Event does not exist: ' + str(eid)), 404
        else:
            response = self._buildEventResponse(eventTuple=event)
            return jsonify(response)
