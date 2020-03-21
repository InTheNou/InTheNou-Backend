from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.EventDAO import EventDAO


def _buildEventResponse(event_tuple):
    response = {}
    response['eid'] = event_tuple[0]
    response['ecreator'] = event_tuple[1]
    response['roomid'] = event_tuple[2]
    response['etitle'] = event_tuple[3]
    response['edescription'] = event_tuple[4]
    response['estart'] = event_tuple[5]
    response['eend'] = event_tuple[6]
    response['ecreation'] = event_tuple[7]
    response['estatus'] = event_tuple[8]
    response['estatusdate'] = event_tuple[9]
    response['photoid'] = event_tuple[10]
    return response


class EventHandler():

    def getEventByID(self, eid):
        """Return the event entry belonging to the specified eid.
        eid -- event ID.
        """
        dao = EventDAO()
        event = dao.getEventByID(eid)
        if not event:
            return jsonify(Error='Event does not exist: eid=' + str(eid)), 404
        else:
            response = _buildEventResponse(event_tuple=event)
            return jsonify(response)
