from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.EventDAO import EventDAO
from app.handlers.RoomHandler import RoomHandler
from app.handlers.TagHandler import TagHandler


def _buildEventResponse(event_tuple):
    """
    Private Method to build event dictionary to be JSONified.
    Parameters:
        event_tuple: response tuple from SQL query
    Returns:
        Dict: Event information.
    """
    response = {}
    response['eid'] = event_tuple[0]
    response['ecreator'] = event_tuple[1]
    response['room'] = RoomHandler().getRoomByID(rid=event_tuple[2], no_json=True)

    # Following line checks if the above returns a json (no room found or no_json set to False.
    if not isinstance(response['room'], dict):
        response['room'] = str(response['room'])

    response['etitle'] = event_tuple[3]
    response['edescription'] = event_tuple[4]
    response['estart'] = event_tuple[5]
    response['eend'] = event_tuple[6]
    response['ecreation'] = event_tuple[7]
    response['estatus'] = event_tuple[8]
    response['estatusdate'] = event_tuple[9]
    response['photourl'] = event_tuple[10]
    response['tags'] = TagHandler().getTagsByEventID(eid=event_tuple[0], no_json=True)

    # Following line checks if the above returns a json (no tags found or no_json set to False.
    if not isinstance(response['tags'], list):
        response['tags'] = str(response['tags'])

    return response


class EventHandler:

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
            print (response)
            return jsonify(response)
