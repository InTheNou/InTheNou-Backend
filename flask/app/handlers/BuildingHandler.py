from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.BuildingDAO import BuildingDAO

ADD_BUILDING_KEYS = ["edificioid", "nomoficial", "blddenom", "codigoold", "bldtype", "attributes"]


def _buildBuildingResponse(building_tuple):
    """
    Private Method to build building dictionary to be JSONified.

     Uses :func:`~app.handlers.BuildingHandler.BuildingHandler._getDistinctFloorNumbersByBuildingID`

    :param building_tuple: response tuple from SQL query
    :returns Dict: Building information with keys:

    .. code-block:: python

        {'bid', 'bname', 'babbrev', 'numfloors', 'bcommonname',
        'btype', 'photourl', 'distinctfloors'}
    """
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

def _buildCoreBuildingResponse(building_tuple):
    """
    Private Method to build building dictionary to be JSONified.

     
    :param building_tuple: response tuple from SQL query
    :returns Dict: Building information with keys:

    .. code-block:: python

        {'bid', 'bname', 'babbrev'}
    """
    # Note: currently using the getBuildingByID() method
    response = {}
    response['bid'] = building_tuple[0]
    response['bname'] = building_tuple[1]
    response['babbrev'] = building_tuple[2]
    return response

def _getDistinctFloorNumbersByBuildingID(bid):
    """
    Private Method to build building dictionary to be JSONified.

     Uses :func:`~app.DAOs.BuildingDAO.BuildingDAO.getDistinctFloorNumbersByBuildingID`

    :param building_tuple: response tuple from SQL query
    :returns Dict: Building information
    """
    floors = BuildingDAO().getDistinctFloorNumbersByBuildingID(bid=bid)
    floor_array = []
    if not floors:
        pass
    else:
        for floor in floors:
            floor_array.append(floor[0])
    return floor_array


class BuildingHandler:

    def addFullBuilding(self, json, uid):
        """
        Handler method to verify that all necessary JSON keys are
        present before creating a new building.
        Uses :func:`~app.DAOs.BuildingDAO.BuildingDAO.addFullBuilding`

        :param json: Contains the necessary keys to create a building from UPRM Portal data
            ["edificioid", "nomoficial", "blddenom", "codigoold", "bldtype", "attributes"]
        :type json: JSON
        :param uid: User ID
        :type uid: int
        :return: JSON
        """
        if not isinstance(uid, int) or uid<0:
            return jsonify(Error="Invalid uid: "+ str(uid))
        for key in ADD_BUILDING_KEYS:
            if key not in json:
                return jsonify(Error='Missing key in JSON: ' + str(key)), 404
        try:
            building_results = BuildingDAO().addFullBuilding(building_json=json, uid=uid)
        except ValueError as e:
            return jsonify(Error=str(e)), 400
        except KeyError as e:
            return jsonify(Error=str(e)), 400
        return jsonify(Result=str(building_results)), 201

    def getAllBuildings(self, no_json=False):
        """
        Return all Building entries in the database.
        Uses :func:`~app.DAOs.BuildingDAO.BuildingDAO.getAllBuildings` as well as
        :func:`~app.handlers.BuildingHandler._buildBuildingResponse`

        :param  no_json: states if the response should be returned as JSON or not. Default=False
        :type no_json: bool
        :return JSON: containing all tags. Error JSON otherwise.
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

    def getAllBuildingsSegmented(self, offset, limit=20):
        """
        Return all Building entries in the database, segmented.
        Uses :func:`~app.DAOs.BuildingDAO.BuildingDAO.getAllBuildingsSegmented` as well as
        :func:`~app.handlers.BuildingHandler._buildBuildingResponse`

        :param offset: Number of results to skip from top of list.
        :type offset: int
        :param limit: Number of results to return. Default = 20.
        :type limit: int
        :return JSON: containing all tags. Error JSON otherwise.
        """
        dao = BuildingDAO()
        buildings = dao.getAllBuildingsSegmented(offset=offset, limit=limit)
        result = []
        for row in buildings:
            result.append(_buildBuildingResponse(row))
        return jsonify(result)

    def getBuildingByID(self, bid, no_json=False):
        """
        Return the building entry belonging to the specified bid.
        Uses :func:`~app.DAOs.BuildingDAO.BuildingDAO.getBuildingByID` as well as
        :func:`~app.handlers.BuildingHandler._buildBuildingResponse`
       

        :param bid: building ID.
        :type bid: int
        :param no_json: states if the response should be returned as JSON or not. Default=False
        :type no_json: bool
        :return JSON: containing room information. Error JSON otherwise.
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
        Uses :func:`~app.DAOs.BuildingDAO.BuildingDAO.getBuildingByID` as well as
        :func:`~app.handlers.BuildingHandler._buildCoreBuildingResponse`
       
        :param bid: building ID.
        :type bid: int
        :param no_json: states if the response should be returned as JSON or not. Default=False
        :type no_json: bool
        :return JSON: containing room information. Error JSON otherwise.
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
        """
        Return the building entry belonging to the specified bid.
        Uses :func:`~app.handlers.BuildingHandler.getBuildingByID` 

        :param bid: building ID.
        :type bid: int
        :return List: containing room information. Error JSON otherwise.
        """
        building = self.getBuildingByID(bid=bid, no_json=True)
        # Following line checks if the above returns a json (no room found or no_json set to False.
        if not isinstance(building, dict):
            building = str(building)
        return building

    def getBuildingsByKeyword(self, offset, limit, keyword):
         """
        Returns a list of buildings taht match a given searchstring
        Uses :func:`~app.DAOs.BuildingDAO.BuildingDAO.searchBuildingsByKeyword`

        :param keyword: The keyword to search for.
        :type keyword: str
        :param offset: Number of results to skip from top of list.
        :type offset: int
        :param limit: Number of results to return. Default = 20.
        :type limit: int
        :return JSON: A list of buildings that match the given keyword
        """
       
         dao = BuildingDAO()
         keyword = keyword
         result = []
         alphanumeric_filter = filter(str.isalnum, keyword)
         keyword = "".join(alphanumeric_filter)
         print(keyword)
         response = dao.searchBuildingsByKeyword(
            keyword=keyword, offset=offset, limit=limit)

         for building in response:
            result.append(_buildBuildingResponse(
                building_tuple=building))

         return jsonify(result)
