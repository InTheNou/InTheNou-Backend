from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.RoomDAO import RoomDAO


def _buildRoomResponse(room_tuple):
    response = {}
    response['rid'] = room_tuple[0]
    response['bid'] = room_tuple[1]
    response['rcode'] = room_tuple[2]
    response['rfloor'] = room_tuple[3]
    response['rdescription'] = room_tuple[4]
    response['roccupancy'] = room_tuple[5]
    response['rdept'] = room_tuple[6]
    response['rcustodian'] = room_tuple[7]
    response['rlongitude'] = float(room_tuple[8])
    response['rlatitude'] = float(room_tuple[9])
    response['raltitude'] = float(room_tuple[10])
    response['photoid'] = room_tuple[11]
    return response


class RoomHandler():

    def getRoomByID(self, rid):
        """
        Return the room entry belonging to the specified rid.
        Parameters:
            rid: room ID.
        Returns:
            JSON: containing room information. Error JSON otherwise.
        """
        dao = RoomDAO()
        room = dao.getRoomByID(rid)
        if not room:
            return jsonify(Error='Room does not exist: ' + str(rid)), 404
        else:
            response = _buildRoomResponse(room_tuple=room)
            return jsonify(response)
