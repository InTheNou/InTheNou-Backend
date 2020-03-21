from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.EventDAO import EventDAO

class EventHandler():

    def _buildEventResponse(self, eventTuple):
        response = {}
        response['eid'] = eventTuple[0]
        response['ecreator'] = eventTuple[1]
        response['roomid'] = eventTuple[2]
        response['etitle'] = eventTuple[3]
        response['edescription'] = eventTuple[4]
        response['estart'] = eventTuple[5]
        response['eend'] = eventTuple[6]
        response['ecreation'] = eventTuple[7]
        response['estatus'] = eventTuple[8]
        response['estatusdate'] = eventTuple[9]
        response['photoid'] = eventTuple[10]
        return response

    def getEventByID(self, eid):
        """Return the event entry belonging to the specified eid.
        eid -- event ID.
        """
        dao = EventDAO()
        event = dao.getEventByID(eid)
        if not event:
            return jsonify(Error='Event does not exist: ' + str(eid)), 404
        else:
            response = self._buildEventResponse(eventTuple=event)
            return jsonify(response)
