from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.BuildingDAO import BuildingDAO


def _buildBuildingResponse(building_tuple):
    response = {}
    response['bid'] = building_tuple[0]
    response['bname'] = building_tuple[1]
    response['numfloors'] = building_tuple[2]
    response['bcommonname'] = building_tuple[3]
    response['btype'] = building_tuple[4]
    response['photourl'] = building_tuple[5]
    return response


class BuildingHandler:

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
            return jsonify(Error='building does not exist: ' + str(bid)), 404
        else:
            response = _buildBuildingResponse(building_tuple=building)
            if no_json:
                return response
            return jsonify(response)
