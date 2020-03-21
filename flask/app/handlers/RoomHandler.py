from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.RoomDAO import RoomDAO


class RoomHandler():

    # def _buildEventResponse(self, eventTuple):
    #     response = {}
    #     response['eid'] = eventTuple[0]
    #     response['ecreator'] = eventTuple[1]
    #     response['roomid'] = eventTuple[2]
    #     response['etitle'] = eventTuple[3]
    #     response['edescription'] = eventTuple[4]
    #     response['estart'] = eventTuple[5]
    #     response['eend'] = eventTuple[6]
    #     response['ecreation'] = eventTuple[7]
    #     response['estatus'] = eventTuple[8]
    #     response['estatusdate'] = eventTuple[9]
    #     response['photoid'] = eventTuple[10]
    #     return response

    def getRoomByID(self, rid):
        """Return the room entry belonging to the specified rid.
        rid -- room ID.
        """
        dao = RoomDAO()
        room = dao.getRoomByID(rid)
        if not room:
            return jsonify(Error='Room does not exist: ' + str(rid)), 404
        else:
            # response = self._buildEventResponse(eventTuple=event)
            # return jsonify()
            return str(room)
