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

    # TODO: Add user information Once Diego creates routes (uid, name, lastname)
    response['ecreator'] = event_tuple[1]
    response['room'] = RoomHandler().safeGetRoomByID(rid=event_tuple[2])
    response['etitle'] = event_tuple[3]
    response['edescription'] = event_tuple[4]
    response['estart'] = event_tuple[5]
    response['eend'] = event_tuple[6]
    response['ecreation'] = event_tuple[7]
    response['estatus'] = event_tuple[8]
    response['estatusdate'] = event_tuple[9]
    response['photourl'] = event_tuple[10]
    response['tags'] = TagHandler().safeGetTagsByEventID(eid=event_tuple[0])
    return response


def _buildCoreEventResponse(event_tuple):
    """
    Private Method to build core event dictionary to be JSONified.
    Parameters:
        event_tuple: response tuple from SQL query
    Returns:
        Dict: Event information.
    """
    response = {}
    response['eid'] = event_tuple[0]
    response['ecreator'] = event_tuple[1]
    response['room'] = RoomHandler().getCoreRoomByID(rid=event_tuple[2], no_json=True)
    response['etitle'] = event_tuple[3]
    response['edescription'] = event_tuple[4]
    response['estart'] = event_tuple[5]
    response['eend'] = event_tuple[6]
    response['ecreation'] = event_tuple[7]
    response['estatus'] = event_tuple[8]
    response['estatusdate'] = event_tuple[9]
    response['photourl'] = event_tuple[10]
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
            return jsonify(response)

    def getUpcomingGeneralEventsSegmented(self, uid, offset, limit=10):
        """Return the upcoming, active event entries specified by offset and limit parameters.
        Parameters:
            uid: User ID
            offset: Number of result rows to ignore from top of query results.
            limit: Max number of result rows to return. Default=10.
        Return:
            JSON Response Object: JSON containing limit-defined number of upcoming, active events.
                """
        dao = EventDAO()
        events = dao.getUpcomingGeneralEventsSegmented(uid=uid, offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            print(events)
            event_list = []
            for row in events:
                event_entry = _buildCoreEventResponse(event_tuple=row)
                # TODO: Consider reworking generalEventsSegmented and builder.
                event_entry['interaction'] = {
                    "itype": row[11],
                    "recommendstatus": row[12]
                }
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getUpcomingFollowedEventsSegmented(self, uid, offset, limit=10):
        """Return the upcoming, active, followed event entries specified by offset and limit parameters.
        Parameters:
            uid: User ID
            offset: Number of result rows to ignore from top of query results.
            limit: Max number of result rows to return. Default=10.
        Return:
            JSON Response Object: JSON containing limit-defined number of upcoming, active events.
                """
        dao = EventDAO()
        events = dao.getUpcomingFollowedEventsSegmented(uid=uid, offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            event_list = []
            for row in events:
                # TODO: consider re-developing Response builders for more flexibility.
                event_entry = _buildCoreEventResponse(event_tuple=row)
                event_entry['recommendstatus'] = row[11]
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)
