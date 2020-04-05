from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.BuildingDAO import BuildingDAO


def _buildBuildingResponse(building_tuple):
    response = {}
    response['bid'] = building_tuple[0]
    response['bname'] = building_tuple[1]
    response['babbrev'] = building_tuple[2]
    response['numfloors'] = building_tuple[3]
    response['bcommonname'] = building_tuple[4]
    response['btype'] = building_tuple[5]
    response['photourl'] = building_tuple[6]
    response['distinctfloors'] = _getDistinctFloorNumbersByBuildingID(
        bid=building_tuple[0])
    return response


def _buildSearchBuildingByKeyword(building_tuple):

    response = {}
    response['bid'] = building_tuple[0]
    response['bname'] = building_tuple[1]
    response['babbrev'] = building_tuple[2]
    response['batype'] = building_tuple[3]
    response['photourl'] = building_tuple[4]
    return response


def _buildCoreBuildingResponse(building_tuple):
    # Note: currently using the getBuildingByID() method
    response = {}
    response['bid'] = building_tuple[0]
    response['bname'] = building_tuple[1]
    response['babbrev'] = building_tuple[2]
    return response


def _getDistinctFloorNumbersByBuildingID(bid):
    floors = BuildingDAO().getDistinctFloorNumbersByBuildingID(bid=bid)
    floor_array = []
    if not floors:
        pass
    else:
        for floor in floors:
            floor_array.append(floor[0])
    return floor_array


class BuildingHandler:

    def getAllBuildings(self, no_json=False):
        """
        Return all Building entries in the database.
        Parameters:
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing all tags. Error JSON otherwise.
        """
        dao = BuildingDAO()
        buildings = dao.getAllBuildings()
        if not buildings:
            return jsonify(Error='Could not find any buildings in system.'), 404
        else:
            building_list = []
            for row in buildings:
                building_list.append(
                    _buildBuildingResponse(building_tuple=row))
            response = {"buildings": building_list}
            if no_json:
                return response
            return jsonify(response)

    def getAllBuildingsSegmented(self, offset, limit):
        dao = BuildingDAO()
        buildings = dao.getAllBuildingsSegmented(offset=offset, limit=limit)
        result = []
        for row in buildings:
            result.append(_buildSearchBuildingByKeyword(row))
        return jsonify(result)

    def getBuildingByID(self, bid, no_json=False):
        """
        Return the building entry belonging to the specified bid.
        Parameters:
            bid: building ID.
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing room information. Error JSON otherwise.
        """
        dao = BuildingDAO()
        building = dao.getBuildingByID(bid=bid)
        if not building:
            return jsonify(Error='building does not exist: bid=' + str(bid)), 404
        else:
            response = _buildBuildingResponse(building_tuple=building)
            if no_json:
                return response
            return jsonify(response)

    def getCoreBuildingByID(self, bid, no_json=False):
        """
        Return the building entry belonging to the specified bid.
        Parameters:
            bid: building ID.
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing room information. Error JSON otherwise.
        """
        dao = BuildingDAO()
        building = dao.getBuildingByID(bid=bid)
        if not building:
            return jsonify(Error='building does not exist: bid=' + str(bid)), 404
        else:
            response = _buildCoreBuildingResponse(building_tuple=building)
            if no_json:
                return response
            return jsonify(response)

    def safeGetBuildingByID(self, bid):
        building = self.getBuildingByID(bid=bid, no_json=True)
        # Following line checks if the above returns a json (no room found or no_json set to False.
        if not isinstance(building, dict):
            building = str(building)
        return building

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

    def getBuildingsByKeyword(self, offset, limit, json):

        dao = BuildingDAO()
        keyword = json['searchstring']
        result = []
        alphanumeric_filter = filter(str.isalnum, keyword)
        keyword = "".join(alphanumeric_filter)

        response = dao.searchBuildingsByKeyword(
            keyword=keyword, offset=offset, limit=limit)

        for building in response:
            result.append(_buildSearchBuildingByKeyword(
                building_tuple=building))

        return jsonify(result)
