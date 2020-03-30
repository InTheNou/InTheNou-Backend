from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.RoomDAO import RoomDAO
from app.handlers.BuildingHandler import BuildingHandler

CHANGEROOMCOORDINATESKEYS = ['rlongitude', 'raltitude', 'rlatitude']


SEARCH_CRITERIA_KEY = 'searchCriteria'
SEARCHSTRING_VALUE = 'searchstring'
ROOMCODE_VALUE = 'rcode'
BABBREV_VALUE = 'babbrev'


# TODO: ADD SERVICES TO A ROOM
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

    # Merging Diego's Service Code into Brian's Room builder.
    # TODO: remove circular dependencies so this import does not occur in here.
    # TODO: Extract error handling.
    from app.handlers.ServiceHandler import ServiceHandler
    services = ServiceHandler().getServicesByRoomID(
        rid=room_tuple[0], no_json=True)
    if not isinstance(services, list):
        services = None
    response['services'] = services
    return response


def _buildCoreRoomResponse(room_tuple):
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


def _buildTinyRoomResponse(room_tuple):
    # Currently using the getRoomByID() method
    response = {}
    response['rid'] = room_tuple[0]
    # Skipping bid so that it may be added either internally
    # as part of a single room, or externally, as part of a
    # list of rooms.
    response['rcode'] = room_tuple[2]
    return response


def _buildChangeCoordinatesRoomResponse(room_tuple):
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
                room_list.append(_buildCoreRoomResponse(room_tuple=row))
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

    def getTinyRoomByID(self, rid, no_json=False):
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
            response = _buildTinyRoomResponse(room_tuple=room)
            response['building'] = BuildingHandler(
            ).getCoreBuildingByID(bid=room[1], no_json=True)
            if no_json:
                return response
            return jsonify(response)

    def changeRoomCoordinates(self, rid, json):
        roomKeys = {}
        for key in json:
            if key in CHANGEROOMCOORDINATESKEYS:
                roomKeys[key] = (json[key])

        dao = RoomDAO()

        response = _buildChangeCoordinatesRoomResponse(
            dao.changeRoomCoordinates(rid=rid, roomKeys=roomKeys))
        if response is not None:
            return jsonify(response)
        else:
            return jsonify(Error="no room was found "), 404

    # copied from Event handler because importing it caused ImportError loop.
    # TODO: merge this, event handler, and others into one importable place.

    def processSearchString(self, searchstring):
        """
        Splits a string by its spaces, filters non-alpha-numeric symbols out,
        and joins the keywords by space-separated pipes.
        """
        keyword_list = str.split(searchstring)
        filtered_words = []
        for word in keyword_list:
            filtered_string = ""
            for character in word:
                if character.isalnum():
                    filtered_string += character
            if not filtered_string.isspace() and filtered_string != "":
                filtered_words.append(filtered_string)
        keywords = " | ".join(filtered_words)
        return keywords

    # TODO: FINISH THIS METHOD, AND MISSING DAO AND ROUTE
    def getRoomsBySearch(self, json, offset, limit=20):
        """
        Return the room entries matching the search parameters.
        Parameters:
            json: JSON object with the key "searchCriteria"
                with values "description" or "roomCode". If "description" is the value,
                the JSON should also have key "searchstring". If "roomCode" is the value,
                the JSON should also have the keys "babbrev" and "rcode".
            offset: Number of result rows to ignore from top of query results.
            limit: Max number of result rows to return. Default=10.
        Returns:
            JSON: containing room information. Error JSON otherwise.
        """
        # Verifying json (needs improvement)
        if json is None:
            return jsonify(Error='No JSON provided'), 401
        if SEARCH_CRITERIA_KEY not in json:
            return jsonify(Error='Key not found: ' + str(SEARCH_CRITERIA_KEY)), 401
        if json[SEARCH_CRITERIA_KEY] == SEARCHSTRING_VALUE:
            if SEARCHSTRING_VALUE not in json:
                return jsonify(Error='Key not found: ' + str(SEARCHSTRING_VALUE)), 401
            search_method = SEARCHSTRING_VALUE
        elif json[SEARCH_CRITERIA_KEY] == ROOMCODE_VALUE:
            if ROOMCODE_VALUE not in json:
                return jsonify(Error='Key not found: ' + str(ROOMCODE_VALUE)), 401
            if BABBREV_VALUE not in json:
                return jsonify(Error='Key not found: ' + str(BABBREV_VALUE)), 401
            search_method = ROOMCODE_VALUE
        else:
            return jsonify(Error='Invalid Search Criteria: ' + str(json[SEARCH_CRITERIA_KEY])), 401

        dao = RoomDAO()
        if search_method == SEARCHSTRING_VALUE:
            keywords = self.processSearchString(
                searchstring=json[SEARCHSTRING_VALUE])
            rooms = dao.getRoomsByKeywordSegmented(
                keywords=keywords, limit=limit, offset=offset)
        else:
            # filtering symbols and spaces out to try and prevent SQL injection.
            # TODO: go over other string routes and check for similar injection vulnerability.
            babbrev = str(json[BABBREV_VALUE]).upper()
            rcode = str(json[ROOMCODE_VALUE])

            alphanumeric_filter = filter(str.isalnum, rcode)
            rcode = "".join(alphanumeric_filter)
            alphanumeric_filter = filter(str.isalnum, babbrev)
            babbrev = "".join(alphanumeric_filter)

            rooms = dao.getRoomsByCodeSearchSegmented(babbrev=babbrev, rcode=rcode,
                                                      limit=limit, offset=offset)
        if not rooms:
            response = {"rooms": None}
        else:
            room_list = []
            for row in rooms:
                room_list.append(_buildCoreRoomResponse(room_tuple=row))
            # TODO:  every room should probably have their building in it.
            response = {"rooms": room_list}
        return jsonify(response)
