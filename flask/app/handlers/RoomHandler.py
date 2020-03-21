from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.RoomDAO import RoomDAO
from app.handlers.BuildingHandler import BuildingHandler


def _buildRoomResponse(room_tuple):
    response = {}
    response['rid'] = room_tuple[0]
    response['building'] = BuildingHandler().getBuildingByID(room_tuple[1], no_json=True)

    # Following line checks if the above returns a json (no room found or no_json set to False.
    if not isinstance(response['building'], dict):
        response['building'] = str(response['building'])

    response['rcode'] = room_tuple[2]
    response['rfloor'] = room_tuple[3]
    response['rdescription'] = room_tuple[4]
    response['roccupancy'] = room_tuple[5]
    response['rdept'] = room_tuple[6]
    response['rcustodian'] = room_tuple[7]
    response['rlongitude'] = float(room_tuple[8])
    response['rlatitude'] = float(room_tuple[9])
    response['raltitude'] = float(room_tuple[10])
    response['photourl'] = room_tuple[11]
    return response


class RoomHandler:

    def getRoomByID(self, rid, no_json=False):
        """
        Return the room entry belonging to the specified rid.
        Parameters:
            rid: room ID.
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing room information. Error JSON otherwise.
        """
        dao = RoomDAO()
        room = dao.getRoomByID(rid)
        if not room:
            return jsonify(Error='Room does not exist: ' + str(rid)), 404
        else:
            response = _buildRoomResponse(room_tuple=room)
            if no_json:
                return response
            return jsonify(response)
