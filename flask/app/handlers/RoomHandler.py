from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.RoomDAO import RoomDAO
from app.handlers.BuildingHandler import BuildingHandler


def _buildRoomResponse(room_tuple):
    response = {}
    response['rid'] = room_tuple[0]
    # Skipping bid so that it may be added either internally
    # as part of a single room, or externally, as part of a
    # list of rooms. Use _safeGetBuiildingByID(bid).
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


def _buildCoreRoomResponse(room_tuple):
    # Currently using the getRoomByID() method
    response = {}
    response['rid'] = room_tuple[0]
    # Skipping bid so that it may be added either internally
    # as part of a single room, or externally, as part of a
    # list of rooms.
    response['rcode'] = room_tuple[2]
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
            response['building'] = BuildingHandler().safeGetBuildingByID(bid=room[1])
            if no_json:
                return response
            return jsonify(response)

    def getRoomsByBuildingAndFloor(self, bid, rfloor, no_json=False):
        """
        Return the room entries belonging to the specified building and floor.
        Parameters:
            bid: building ID.
            rfloor: room floor.
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing room information. Error JSON otherwise.
        """
        dao = RoomDAO()
        rooms = dao.getRoomsByBuildingAndFloor(bid=bid, rfloor=rfloor)
        if not rooms:
            return jsonify(Error='No rooms found for bid=' + str(bid)
                                 + " and rfloor=" + str(rfloor)), 404
        else:
            room_list = []
            for row in rooms:
                room_list.append(_buildRoomResponse(room_tuple=row))
            response = {"rooms": room_list,
                        'building': BuildingHandler().safeGetBuildingByID(bid=bid)}
        if no_json:
            return response
        return jsonify(response)

    def safeGetRoomByID(self, rid):
        room = self.getRoomByID(rid=rid, no_json=True)
        # Following line checks if the above returns a json (no room found or no_json set to False.
        if not isinstance(room, dict):
            room = str(room)
        return room

    def getCoreRoomByID(self, rid, no_json=False):
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
            response = _buildCoreRoomResponse(room_tuple=room)
            response['building'] = BuildingHandler().getCoreBuildingByID(bid=room[1], no_json=True)
            if no_json:
                return response
            return jsonify(response)
