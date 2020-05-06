from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.RoomDAO import RoomDAO
from app.handlers.BuildingHandler import BuildingHandler
import app.handlers.SharedValidationFunctions as SVF

CHANGEROOMCOORDINATESKEYS = ['rlongitude', 'raltitude', 'rlatitude']


# TODO: remove circular dependencies so this import does not occur in here.
def _buildRoomResponse(room_tuple):
    """
    Private Method to build room dictionary to be JSONified.

     Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.GetServicesByRoomID`

    :param room_tuple: response tuple from SQL query
    :returns Dict: Room information with keys:

    .. code-block:: python

        {'rid',  'rcode', 'rdescription', 'roccupancy',
        'rdept', 'rcustodian','rlongitude','rlatitude','raltitude','photourl'}
    """
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

    # Merging Diego's Service Code into Brian's Room builder.
    # TODO: Extract error handling.
    from app.handlers.ServiceHandler import ServiceHandler
    services = ServiceHandler().getServicesByRoomID(
        rid=room_tuple[0], no_json=True)
    if not isinstance(services, list):
        services = None
    response['services'] = services
    return response


def _buildCoreRoomResponse(room_tuple):
    """
    Private Method to build core room dictionary to be JSONified.

     
    :param room_tuple: response tuple from SQL query
    :returns Dict: Room information with keys:

    .. code-block:: python

        {'rid',  'rcode','rfloor' ,'rdescription', 'roccupancy',
        'rdept', 'rcustodian','rlongitude','rlatitude','raltitude','photourl'}
    """
    response = {}
    response['rid'] = room_tuple[0]
    # Skipping bid so that it may be added either internally
    # as part of a single room, or externally, as part of a
    # list of rooms. Use _safeGetBuiildingByID(bid).
    response['rcode'] = str(room_tuple[2])
    response['rfloor'] = room_tuple[3]
    response['rdescription'] = room_tuple[4]
    response['roccupancy'] = room_tuple[5]
    response['rdept'] = room_tuple[6]
    response['rcustodian'] = str(room_tuple[7])
    response['rlongitude'] = float(room_tuple[8])
    response['rlatitude'] = float(room_tuple[9])
    response['raltitude'] = float(room_tuple[10])
    response['photourl'] = room_tuple[11]
    return response


def _buildTinyRoomResponse(room_tuple):
    """
    Private Method to build minimal room dictionary to be JSONified.

     
    :param room_tuple: response tuple from SQL query
    :returns Dict: Room information with keys:

    .. code-block:: python

        {'rid',  'rcode'}
    """
    # Currently using the getRoomByID() method
    response = {}
    response['rid'] = room_tuple[0]
    # Skipping bid so that it may be added either internally
    # as part of a single room, or externally, as part of a
    # list of rooms.
    response['rcode'] = room_tuple[2]
    return response


def _buildChangeCoordinatesRoomResponse(room_tuple):
    """
    Private Method to build change coordinates of a room dictionary to be JSONified.

    :param room_tuple: response tuple from SQL query
    :returns Dict: Room information with keys:

    .. code-block:: python

        {'rid',  'rcode','rfloor',
        'rlongitude','rlatitude','raltitude'}
    """
    # Currently using the getRoomByID() method
    response = {}
    response['rid'] = room_tuple[0]
    response['rcode'] = room_tuple[1]
    response['rfloor'] = room_tuple[2]
    response['rlongitude'] = float(room_tuple[3])
    response['rlatitude'] = float(room_tuple[4])
    response['raltitude'] = float(room_tuple[5])

    return response


class RoomHandler:

    def getRoomByID(self, rid, no_json=False):
        """
        Return the room entry belonging to the specified rid.

        :param rid: room ID.
        :param no_json: states if the response should be returned as JSON or not.
        :return JSON: containing room information. Error JSON otherwise.
        """
        dao = RoomDAO()
        room = dao.getRoomByID(rid)
        if not room:
            return jsonify(Error='Room does not exist: ' + str(rid)), 404
        else:
            if no_json:
                response = _buildCoreRoomResponse(room_tuple=room)
            else:
                response = _buildRoomResponse(room_tuple=room)
            response['building'] = BuildingHandler(
            ).safeGetBuildingByID(bid=room[1])
            if no_json:
                return response
            return jsonify(response)

    def getRoomsByBuildingAndFloor(self, bid, rfloor, no_json=False):
        """
        Return the room entries belonging to the specified building and floor.

        :param  bid: building ID.
        :param  rfloor: room floor.
        :param no_json: states if the response should be returned as JSON or not.
        :return JSON: containing room information. Error JSON otherwise.
        """
        dao = RoomDAO()
        rooms = dao.getRoomsByBuildingAndFloor(bid=bid, rfloor=rfloor)
        if not rooms:
            return jsonify(Error='No rooms found for bid=' + str(bid)
                                 + " and rfloor=" + str(rfloor)), 404
        else:
            room_list = []
            for row in rooms:
                room_list.append(_buildCoreRoomResponse(room_tuple=row))
            response = {"rooms": room_list,
                        'building': BuildingHandler().safeGetBuildingByID(bid=bid)}
        if no_json:
            return response
        return jsonify(response)

    def safeGetRoomByID(self, rid):
        """
        Return a room given the room ID

        :param rid: room ID.
        :return JSON: containing room information. Error JSON otherwise.
        """
        room = self.getRoomByID(rid=rid, no_json=True)
        # Following line checks if the above returns a json (no room found or no_json set to False.
        if not isinstance(room, dict):
            room = str(room)
        return room

    def getTinyRoomByID(self, rid, no_json=False):
        """
        Return the room entry belonging to the specified rid.

        :param rid: room ID.
        :param  no_json: states if the response should be returned as JSON or not.
        :return JSON: containing room information. Error JSON otherwise.
        """
        dao = RoomDAO()
        room = dao.getRoomByID(rid)
        if not room:
            return jsonify(Error='Room does not exist: ' + str(rid)), 404
        else:
            response = _buildTinyRoomResponse(room_tuple=room)
            response['building'] = BuildingHandler(
            ).getCoreBuildingByID(bid=room[1], no_json=True)
            if no_json:
                return response
            return jsonify(response)

    def changeRoomCoordinates(self, rid, json, uid):
        """
        Edit a room's coordinates given the room ID

        :param rid: Room ID.
        :param uid: User ID
        :param  json: json payload with the following keys:

                * rlatitude
                * rlongitude
                * raltitude

        :return JSON: containing room information. Error JSON otherwise.
        """
        roomKeys = {}
        for key in json:
            if key in CHANGEROOMCOORDINATESKEYS:
                roomKeys[key] = (json[key])

        dao = RoomDAO()
        room = dao.changeRoomCoordinates(rid=rid, roomKeys=roomKeys, uid=uid)
        if room is not None:
            response = _buildChangeCoordinatesRoomResponse(room)
            return jsonify(response)
        else:
            return jsonify(Error="no room was found "), 404

    def getRoomsByKeywordSegmented(self, searchstring, offset, limit=20):
        """
        Return the room entries matching the search parameters.

        :param  searchstring: string separated by whitespaces with terms to search for
        :param offset: Number of result rows to ignore from top of query results.
        :param limit: Max number of result rows to return. Default=20.
        :return JSON: containing room information or null. Error JSON otherwise.
        """
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
            keywords = SVF.processSearchString(searchstring=searchstring)
        except KeyError as e:
            return jsonify(Error=str(e)), 400
        except ValueError as e:
            return jsonify(Error=str(e)), 400

        dao = RoomDAO()
        rooms = dao.getRoomsByKeywordSegmented(
            keywords=keywords, limit=limit, offset=offset)
        if not rooms:
            response = {"rooms": None}
        else:
            room_list = []
            for row in rooms:
                room_result = _buildCoreRoomResponse(room_tuple=row)
                room_result['building'] = BuildingHandler().getCoreBuildingByID(bid=row[1], no_json=True)
                room_list.append(room_result)
            response = {"rooms": room_list}
        return jsonify(response)

    def getRoomsByCodeSearchSegmented(self, babbrev, rcode, offset, limit=20):
        """
        Return the room entries matching the search parameters.

        :param babbrev: string corresponding to the building abbreviation
        :param rcode: string corresponding to the room code
        :param offset: Number of result rows to ignore from top of query results.
        :param limit: Max number of result rows to return. Default=20.
        :return JSON: containing room information or null. Error JSON otherwise.
        """
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
        except KeyError as e:
            return jsonify(Error=str(e)), 400
        except ValueError as e:
            return jsonify(Error=str(e)), 400

        # Filter strings.
        # Force sent abbrev and rcode to be strings appropriate for LIKE query.
        babbrev = str(babbrev).upper()
        rcode = str(rcode)

        # Remove symbols and spaces from strings. Leave only numbers and letters.
        rcode = "".join(filter(str.isalnum, rcode))
        babbrev = "".join(filter(str.isalnum, babbrev))

        dao = RoomDAO()
        rooms = dao.getRoomsByCodeSearchSegmented(
            babbrev=babbrev, rcode=rcode, limit=limit, offset=offset)

        if not rooms:
            response = {"rooms": None}
        else:
            room_list = []
            for row in rooms:
                room_result = _buildCoreRoomResponse(room_tuple=row)
                room_result['building'] = BuildingHandler().getCoreBuildingByID(bid=row[1], no_json=True)
                room_list.append(room_result)
            response = {"rooms": room_list}
        return jsonify(response)
