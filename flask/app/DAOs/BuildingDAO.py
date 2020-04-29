from app.DAOs.MasterDAO import MasterDAO
from app.DAOs.AuditDAO import AuditDAO
from psycopg2 import sql, errors
from psycopg2.extensions import AsIs
import requests

STANDARD_HEIGHT = 35
AVG_STORY_HEIGHT = 2
BUILDING_TYPES = {
  "1":"Académico",
  "2": "Administrativo",
  "9": "Espacio Abierto",
  "13": "Investigación",
  "14": "Agricultura",
  "15": "Facilidades de Animales"
}
DEFAULT_COORDINATES = [0.00, 0.00]

CTI_ROOMS_URL = "https://portal.upr.edu/rum/buildings/export.php?op1=1&building="


def _build_building_insert_sql(building_data):
    """
    Private method that does some light parameter verification
    on the expected building JSON and creates the insert query
    to be used to create a new building.

    :param building_data: dictionary that contains the needed CTI key-value pairs.
    :type building_data: dict
    :return str: Query to insert Building.
    :raises ValueError: Invalid number of floors.
    :raises KeyError: Missing key in data.
    """
    numfloors = -1
    photoid = "Null"

    try:
        bname = building_data["nomoficial"]
        babbrev = building_data["codigoold"]
        bcommonname = building_data["blddenom"]
        btype = BUILDING_TYPES[building_data["bldtype"]]

        for attribute in building_data["attributes"]:
            if attribute[0] == "1":
                numfloors = int(attribute[1])
        if numfloors <= 0:
            raise ValueError("Invalid or missing numfloors value: " + str(numfloors))
    except KeyError as bk:
        raise KeyError("Key not found in building_data: " + str(bk))

    insert_building_query = "Insert into buildings(bname, babbrev, numfloors, bcommonname, btype, photoid) " \
                            "values('{bname}', '{babbrev}', {numfloors}, '{bcommonname}', '{btype}', {photoid}) " \
                            "on conflict(bname) do update set babbrev='{babbrev}', numfloors={numfloors}, " \
                            "bcommonname='{bcommonname}', btype='{btype}' returning bid;".format(
        bname=bname, babbrev=babbrev, numfloors=numfloors, bcommonname=bcommonname, btype=btype, photoid=photoid)

    return insert_building_query


def _build_insert_room_sql(building_data):
    """
    Does some heavier parameter verification on the building data, calls the UPRM Portal API,
    and collects the room data for a given building ID.

    :param building_data: dictionary that contains the needed CTI key-value pairs.
    :type building_data: dict
    :return list: list of queries to insert all rooms in a given building.
    :raises KeyError: missing key in building data.
    :raises ValueError: Given building name does not match the building name found in the Portal data.
    """
    try:
        bname = building_data["nomoficial"]
        babbrev = building_data["codigoold"]
        building_id = int(building_data['edificioid'])
        building_cooridnates = DEFAULT_COORDINATES

        for attribute in building_data["attributes"]:
            if attribute[0] == "15":
                split_coords = attribute[1].split(",")
                building_cooridnates = [float(split_coords[0]), float(split_coords[1])]
        if building_cooridnates == DEFAULT_COORDINATES:
            print("Attribute '15' (building cooridnates) not found in 'attributes' value in building_data;\n"
                  "default values will be used: " + str(building_cooridnates))
    except KeyError as bk:
        raise KeyError("Key not found in building_data: " + str(bk))

    print("Issuing GET to: " + str(CTI_ROOMS_URL + str(building_id)))
    r = requests.get(url=(CTI_ROOMS_URL + str(building_id)))

    # extracting data in json format
    building_rooms_data = r.json()

    print("Received response.")

    roomcodes = []
    list_of_queries= []
    for room in building_rooms_data:
        try:
            rcode = room["space_num"]
            rfloor = room["num_piso"]
            if not rfloor.isnumeric():
                print("Room Floor is invalid: " + str(rfloor) + ", Skipping room insertion.\n")
                continue
            rfloor = int(rfloor)
            rdescription = room["descsp"]
            roccupancy = int(room["capacity"])
            rdept = room["department"]
            rcustodian = room["nombre_contacto"]
            rlatitude = building_cooridnates[0]
            rlongitude = building_cooridnates[1]
            raltitude = STANDARD_HEIGHT + (AVG_STORY_HEIGHT * rfloor)
            room_building = room['nomoficial']
        except KeyError as bk:
            raise KeyError("Key not found in building_rooms_data: " + str(bk))

        if not rcode or rcode.isspace():
            print("Entry with missing rcode found for building: " + str(bname) + ".\nRelated fields: " + str(room))
            print("Skipping Room Insertion.\n")
        elif rcode in roomcodes:
            # TODO: if inserting directly, consider on conflict, update to new info.
            # raise ValueError("Duplicate room code in Data: " + str(insert_room_query))
            print("Duplicate Room Code found in building " + str(bname) + ": " + str(babbrev) + "-" + str(
                rcode) + ".\nSkipping room insertion\n")
        elif not rdept or rdept.isspace():
            print("No department assigned to room entry: " + str(room))
            print("Inserting anyway.")
            # raise ValueError("No department assigned to room entry: " + str(room))
        elif bname not in room_building:
            raise ValueError("Building name provided (" + str(bname) + ") does not match the one recieved in the room (" + str(room_building) + ").")
        else:

            insert_room_query = "Insert into rooms(bid, rcode, rfloor, rdescription, " \
                                "roccupancy, rdept, rcustodian, rlongitude, rlatitude, " \
                                "raltitude, photoid) " \
                                "values(" \
                                "(SELECT bid FROM buildings WHERE bname='{bname}')," \
                                "'{rcode}',{rfloor},'{rdescription}',{roccupancy},'{rdept}'," \
                                "'{rcustodian}',{rlongitude}, {rlatitude}, {raltitude}, NULL) " \
                                "on conflict (bid, rcode) " \
                                "do update set rfloor={rfloor}, rdescription='{rdescription}', " \
                                "roccupancy={roccupancy}, rdept='{rdept}', rcustodian='{rcustodian}';".format(
                bname=bname, rcode=rcode, rfloor=rfloor, rdescription=rdescription, roccupancy=roccupancy,
                rdept=rdept, rcustodian=rcustodian, rlongitude=rlongitude, rlatitude=rlatitude, raltitude=raltitude)

            list_of_queries.append(insert_room_query)
            roomcodes.append(rcode)

    return list_of_queries


class BuildingDAO(MasterDAO):

    def addFullBuilding(self, building_json, uid):
        """
        Executes queries needed to create a new building or update an existing building
        with information from the UPRM Portal database.

        Uses the private methods :ref:`~app.DAOs.BuildingDAO.BuildingDAO._build_building_insert_sql`
        and :ref:`~app.DAOs.BuildingDAO.BuildingDAO._build_insert_room_sql`

        :param building_json: dictionary that contains the needed CTI key-value pairs.
        :type building_data: dict
        :param uid: User ID
        :type uid: int
        :return: Success response with old bid.
        """

        # Assuming json is valid.
        building_query = _build_building_insert_sql(building_data=building_json)
        rooms_queries = _build_insert_room_sql(building_data=building_json)

        cursor = self.conn.cursor()
        try:
            audit = AuditDAO()
            tablename = "buildings"
            pkey = "bname"
            oldValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=building_json["nomoficial"],
                                                  cursor=cursor)

            old_bid = cursor.execute(building_query)
            newValue = audit.getTableValueByIntID(table=tablename, pkeyname=pkey, pkeyval=building_json["nomoficial"],
                                                  cursor=cursor)
            audit.insertAuditEntry(changedTable=tablename, changeType=audit.INSERTVALUE, oldValue=oldValue,
                                   newValue=newValue, uid=uid, cursor=cursor)
            selectquery = "select * from rooms where bid=(SELECT bid FROM buildings " \
                       "WHERE bname='{bname}')".format(bname=building_json["nomoficial"])
            oldvalue = str(cursor.execute(selectquery))
            for query in rooms_queries:
                try:
                    cursor.execute("savepoint my_save_point")
                    cursor.execute(query)
                except errors.CheckViolation as cv:
                    cursor.execute("rollback to savepoint my_save_point")
                    print("CheckViolation raised; continuing execution.\nError message: " + str(cv))
                finally:
                    cursor.execute("release savepoint my_save_point")
            newValue = str(cursor.execute(selectquery))
            audit.insertAuditEntry(changedTable="rooms", changeType=audit.INSERTVALUE, oldValue=oldValue,
                                   newValue=newValue, uid=uid, cursor=cursor)

            self.conn.commit()
            self.conn.close()
            response = "Building Added successfuly: " + str(building_json["nomoficial"]) + ".\nOld bid = " + str(old_bid)

            return response
        except:
            self.conn.rollback()
            self.conn.close()
            raise

    def getAllBuildingsSegmented(self, limit, offset):
        """
        Returns a list of all buildings in the system, segmented
        Params:
        limit: The amount of records to ignore 
        offset: The amount of rows to return in the list  
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "offset %s limit %s ").format(
            fields=sql.SQL(',').join([
                sql.Identifier('bid'),
                sql.Identifier('bname'),
                sql.Identifier('babbrev'),
                sql.Identifier('numfloors'),
                sql.Identifier('bcommonname'),
                sql.Identifier('btype'),
                sql.Identifier('photourl')
            ]),
            table1=sql.Identifier('buildings'),
            table2=sql.Identifier('photos'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'))
        cursor.execute(query, (offset, limit))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAllBuildings(self):
        """
                Query Database for all Building entries.
               Returns:
                   Tuple: SQL result of Query as a tuple.
               """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier};").format(
            fields=sql.SQL(',').join([
                sql.Identifier('bid'),
                sql.Identifier('bname'),
                sql.Identifier('babbrev'),
                sql.Identifier('numfloors'),
                sql.Identifier('bcommonname'),
                sql.Identifier('btype'),
                sql.Identifier('photourl')
            ]),
            table1=sql.Identifier('buildings'),
            table2=sql.Identifier('photos'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'))
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getBuildingByID(self, bid):
        """
                Query Database for an Building's information by its bid.
               Parameters:
                   bid: building ID
               Returns:
                   Tuple: SQL result of Query as a tuple.
               """
        cursor = self.conn.cursor()
        query = sql.SQL("select {fields} from {table1} "
                        "left outer join {table2} "
                        "on {table1}.{table1Identifier} = {table2}.{table2Identifier} "
                        "where {pkey}= %s;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('bid'),
                sql.Identifier('bname'),
                sql.Identifier('babbrev'),
                sql.Identifier('numfloors'),
                sql.Identifier('bcommonname'),
                sql.Identifier('btype'),
                sql.Identifier('photourl')
            ]),
            table1=sql.Identifier('buildings'),
            table2=sql.Identifier('photos'),
            table1Identifier=sql.Identifier('photoid'),
            table2Identifier=sql.Identifier('photoid'),
            pkey=sql.Identifier('bid'))
        cursor.execute(query, (int(bid),))
        result = cursor.fetchone()
        return result

    def getDistinctFloorNumbersByBuildingID(self, bid):
        """
        gets a list of distinct floors given a building ID
        Parameters:
        bid: The building ID to get the distinct floors from
        """
        cursor = self.conn.cursor()
        query = sql.SQL("select distinct rfloor "
                        "from {table} "
                        "where {pkey}=%s "
                        "order by rfloor;").format(
            fields=sql.SQL(',').join([
                sql.Identifier('rfloor')
            ]),
            table=sql.Identifier('rooms'),
            pkey=sql.Identifier('bid'))
        cursor.execute(query, (int(bid),))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def searchBuildingsByKeyword(self, offset, limit, keyword):
        """
        Returns Buildings list that contain some keyword 
        prameters:
        Keyword: word to filter buildings with
        limit: The amount of records to ignore 
        offset: The amount of rows to return in the list  
        """
        keyword = "'%" + keyword + "%'"
        keyword = AsIs(keyword)
        print(keyword)
        cursor = self.conn.cursor()
        query = sql.SQL("select DISTINCT {fields} "
                        "from {table} left outer join {table2} "
                        "on( photos.photoid = buildings.photoid ) where( bname like UPPER ( %s  ) or babbrev like UPPER ( %s  ) or bcommonname like UPPER ( %s  ) ) "
                        "offset %s limit %s ").format(
            fields=sql.SQL(',').join([
                sql.Identifier('bid'),
                sql.Identifier('bname'),
                sql.Identifier('babbrev'),
                sql.Identifier('numfloors'),
                sql.Identifier('bcommonname'),
                sql.Identifier('btype'),
                sql.Identifier('photourl')
            ]),
            table=sql.Identifier('buildings'),
            table2=sql.Identifier('photos'))
        cursor.execute(query, ((keyword), (keyword),(keyword), offset, limit))
        result = []
        for row in cursor:
            result.append(row)
            print(result)
        return result
