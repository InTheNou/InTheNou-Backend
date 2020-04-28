from flask import jsonify,Response
from flask_login import current_user
from psycopg2 import IntegrityError
from app.DAOs.ServiceDAO import ServiceDAO
from app.DAOs.WebsiteDAO import WebsiteDAO
from app.DAOs.PhoneDAO import PhoneDAO
from app.handlers.RoomHandler import RoomHandler
from app.handlers.WebsiteHandler import WebsiteHandler
from app.handlers.PhoneHandler import PhoneHandler
import app.handlers.SharedValidationFunctions as SVF


CREATESERVICEKEYS = ['uid', 'rid', 'sname',
                     'sdescription', 'sschedule', 'PNumbers', 'Websites']
UPDATESERVICEKEYS = ['sname', 'sdescription', 'sschedule', 'rid']
SEARCHSTRING_VALUE = 'searchstring'





def _buildServiceResponse(service_tuple):
    """
    Private Method to build service dictionary to be JSONified.

     Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.safeGetServiceByRoomID`

    :param service_tuple: response tuple from SQL query
    :returns Dict: Service information with keys:

    .. code-block:: python

        {'sid',  'room', 'sname', 'sdescription',
        'sschedule', 'isdeleted'}
    """
    response = {}
    response['sid'] = service_tuple[0]
    response['room'] = RoomHandler().safeGetRoomByID(rid=service_tuple[1])
    response['sname'] = str(service_tuple[2])
    response['sdescription'] = str(service_tuple[3])
    response['sschedule'] = service_tuple[4]
    response['isdeleted'] = service_tuple[5]
    return response


def _buildCoreServiceResponse(service_tuple):
    """
    Private Method to build core service dictionary to be JSONified.

     Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.safeGetServiceByRoomID`

    :param service_tuple: response tuple from SQL query
    :returns Dict: Service information with keys:

    .. code-block:: python

        {'sid',  'rid', 'sname', 'sdescription',
        'sschedule'}
    """
    response = {}
    response['sid'] = service_tuple[0]
    response['rid'] = RoomHandler().safeGetRoomByID(rid=service_tuple[1])
    response['sname'] = service_tuple[2]
    response['sdescription'] = service_tuple[3]
    response['sschedule'] = service_tuple[4]

    return response


def _buildServiceByRoomResponse(service_tuple):
    """
    Private Method to build service dictionary from a given room ID to be JSONified.

     Uses :
     
     * :func:`~app.handlers.PhoneHandler.PhoneHandler.getPhonesByServiceID`
     * :func:`~app.handlers.WebsiteHandler.WebsiteHandler.getWebsitesByServiceID`
     
    :param service_tuple: response tuple from SQL query
    :returns Dict: Service information with keys:

    .. code-block:: python

        {'sid', 'sname', 'sdescription',
        'sschedule', 'PNumbers','Websites'}
    """
    response = {}
    response['sid'] = service_tuple[0]
    response['sname'] = service_tuple[1]
    response['sdescription'] = service_tuple[2]
    response['sschedule'] = service_tuple[3]
    response['PNumbers'] = PhoneHandler().getPhonesByServiceID(
                sid=service_tuple[0], no_json=True)
    response['Websites'] = WebsiteHandler().getWebistesByServiceID(
                sid=service_tuple[0], no_json=True)
    return response


class ServiceHandler:
    """
    Handler Class to manage getting/creating/modifying services
    """
    def createService(self, json,uid):
        """Attempt to create a service.

         Uses :func:`~app.DAOs.ServiceDAO.ServiceDAO.createService` as well as:

         * :func:`~app.handlers.PhoneHandler.PhoneHandler.unpackPhones`
         * :func:`~app.handlers.WebsiteHandler.WebsiteHandler.unpackWebsites`
         
         :param uid: User ID.
         :type uid: int
         :param json: JSON object with the following keys:

                * rid (room ID)
                * sname
                * sdescription
                * sschedule
                * Websites
                * PNumbers
            

        :type json: JSON
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        
         # TODO:SHOULD TAKE PARAMETERS DINAMICALLY CHECKING FOR KEYS
        for key in CREATESERVICEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
      
        websites = WebsiteHandler().unpackWebsites(json=json['Websites'])
        if len(websites) > 10:
            return jsonify(Error="Improper number of websites provided: " + str(len(websites))), 400
        
        
        phones = PhoneHandler().unpackPhones(json=json['PNumbers'])
        if len(websites) > 10:
            return jsonify(Error="Improper number of websites provided: " + str(len(websites))), 400

        # MAKE DICTIONARY TO CRREATE THESE
        user = uid
        roomID = json['rid']
        name = json['sname']
        description = json['sdescription']
        schedule = json['sschedule']

        dao = ServiceDAO()
        service = dao.createService(uid=user,
                                    rid=roomID,
                                    sname=name,
                                    sdescription=description,
                                    sschedule=schedule,
                                    websites=websites,
                                    numbers=phones
                                    )
        try:
            sid = service[0]
        except TypeError:
                return jsonify(Error="Error in input Parameters" ), 400
        
        if isinstance(service, Response):
            return service
        
        else:
            return self.getServiceByID(sid)

    def deleteService(self, sid, uid):
        """Attempt to delete a service.

        Uses :func:`~app.DAOs.ServiceDAO.ServiceDAO.deleteService`
        :param uid: User ID.
        :type uid: int
        :param sid: Service ID.
        :type uid: int
        
                * rid (room ID)
                * sname
                * sdescription
                * sschedule
                * Websites
                * PNumbers
            

        :type json: JSON
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        dao = ServiceDAO()
        service = dao.deleteService(sid, uid=uid)
        if service is not None:
            return jsonify(_buildCoreServiceResponse(service))
        return jsonify(Error="No service with that ID"), 404

    def getServiceByID(self, sid, no_json=False):
        """Return the Service entry belonging to the specified sid.

        Uses :func:`~app.DAOs.ServiceDAO.ServiceDAO.getServiceByID` as well as
        :func:`~app.handlers.ServiceHandler._buildCoreServiceResponse`

        :param sid: Service ID
        :type sid: int
        :param no_json: States whether or not to return the successful response as a dictionary.
        :type no_json: bool
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        Phonehandler = PhoneHandler()
        Websitehandler = WebsiteHandler()
        dao = ServiceDAO()
        service = dao.getServiceByID(sid=sid)
        if not service:
            return jsonify(Error='Service does not exist: sid=' + str(sid)), 404
        else:
            response = _buildServiceResponse(service_tuple=service)
            response['PNumbers'] = Phonehandler.getPhonesByServiceID(
                sid=sid, no_json=True)
            response['Websites'] = Websitehandler.getWebistesByServiceID(
                sid=sid, no_json=True)
            if no_json:
                return response
            return jsonify(response)

    def getServicesByRoomID(self, rid, no_json=False):
        """Return the Service entry belonging to the specified rid.
        
        Uses :func:`~app.DAOs.ServiceDAO.ServiceDAO.getServiceByRoomID` as well as
        :func:`~app.handlers.ServiceHandler._buildServiceByRoomResponse`

        :param rid: Room ID
        :type rid: int
        :param no_json: States whether or not to return the successful response as a dictionary.
        :type no_json: bool
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        
        dao = ServiceDAO()
        services = dao.getServicesByRoomID(rid=rid)
        serviceInfo = []
        for row in services:
            serviceInfo.append(_buildServiceByRoomResponse(row))
            
        if no_json:
            return(serviceInfo)
        
        if len(serviceInfo) > 0:
            return jsonify({"Services": serviceInfo})
        else:
            return jsonify({"Services": None})

    def getServicesSegmented(self, offset, limit):
        """Get all services, segmented

         Uses :func:`~app.DAOs.EventDAO.ServiceDAO.getAllServicesSegmented` as well as:

             * :func:`~app.handlers.SharedValidationFunctions.validate_offset_limit`
             * :func:`~app.handlers.EventHandler._buildCoreServiceResponse`

        :param offset: Number of results to skip from top of list.
        :type offset: int
        :param limit: Number of results to return. Default = 20.
        :type limit: int
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400

        dao = ServiceDAO()

        services = dao.getServicesSegmented(offset=offset, limit=limit)
        if not services:
            response = {'Services': None}
        else:
            service_list = []
            for row in services:
                service_list.append(_buildCoreServiceResponse(row))
            response = {'Services': service_list}
            return jsonify(response)

    def updateServiceInformation(self, sid, json, uid):
        """Attempt to update a service.

         Uses :func:`~app.DAOs.ServiceDAO.ServiceDAO.createService` as well as:

         * :func:`~app.handlers.PhoneHandler.PhoneHandler.unpackPhones`
         * :func:`~app.handlers.WebsiteHandler.WebsiteHandler.unpackWebsites`
         
         :param uid: User ID.
         :type uid: int
         :param json: JSON object with the following keys:

                * rid (room ID)
                * sname
                * sdescription
                * sschedule
                * Websites
                * PNumbers
            

         :type json: JSON
         :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        service = {}
        for key in json:
            if key in UPDATESERVICEKEYS:
                service[key] = (json[key])
        dao = ServiceDAO()

        id = dao.updateServiceInformation(service=service, sid=sid, uid=uid)

        if id is not None:
            response = _buildServiceResponse(dao.getServiceByID(id[0]))

            return jsonify(response)
        else:
            return jsonify(Error="no service with that ID found")

    def getServicesByKeywords(self, searchstring, offset, limit=20):
        """Get all services by keyword, segmented

         Uses :func:`~app.DAOs.EventDAO.ServiceDAO.getServicesByKeywords` as well as:

          
             * :func:`~app.handlers.EventHandler._buildServiceResponse`
        
        :param searchstring: Keyword to search for services.
        :type offset: string
        :param offset: Number of results to skip from top of list.
        :type offset: int
        :param limit: Number of results to return. Default = 20.
        :type limit: int
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
            keywords = SVF.processSearchString(
                searchstring=searchstring)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400

        dao = ServiceDAO()
        services = dao.getServicesByKeywords(
            searchstring=keywords, offset=offset, limit=limit)
        if not services:
            response = {'services': None}
        else:
            service_list = []
            for row in services:
                service_list.append(_buildServiceResponse(service_tuple=row))
            response = {'services': service_list}
        return jsonify(response)
