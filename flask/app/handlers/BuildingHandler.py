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
    return response


class BuildingHandler:

    def getAllBuildings(self, no_json=False):
        """
        Return all tag entries in the database.
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
                building_list.append(_buildBuildingResponse(building_tuple=row))
            response = {"buildings": building_list}
            if no_json:
                return response
            return jsonify(response)

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

    def safeGetBuildingByID(self, bid):
        building = self.getBuildingByID(bid=bid, no_json=True)
        # Following line checks if the above returns a json (no room found or no_json set to False.
        if not isinstance(building, dict):
            building = str(building)
        return building
