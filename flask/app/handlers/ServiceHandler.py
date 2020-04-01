from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.ServiceDAO import ServiceDAO
from app.DAOs.WebsiteDAO import WebsiteDAO
from app.DAOs.PhoneDAO import PhoneDAO
from app.handlers.RoomHandler import RoomHandler
from app.handlers.WebsiteHandler import WebsiteHandler
from app.handlers.PhoneHandler import PhoneHandler


CREATESERVICEKEYS = ['uid', 'rid', 'sname',
                     'sdescription', 'sschedule', 'PNumbers', 'Websites']
UPDATESERVICEKEYS = ['sname', 'sdescription', 'sschedule', 'rid']

SEARCHSTRING_VALUE = 'searchstring'


def _buildPhoneResponse(phone_tuple):
    response = {}
    response['phoneid'] = phone_tuple[0]
    response['pnumber'] = phone_tuple[1]
    response['ptype'] = phone_tuple[2]

    return response


def _buildServiceResponse(service_tuple):
    response = {}
    response['sid'] = service_tuple[0]
    response['room'] = RoomHandler().safeGetRoomByID(rid=service_tuple[1])
    response['sname'] = service_tuple[2]
    response['sdescription'] = service_tuple[3]
    response['sschedule'] = service_tuple[4]
    response['isdeleted'] = service_tuple[5]
    return response


def _buildCoreServiceResponse(service_tuple):
    response = {}
    response['sid'] = service_tuple[0]
    response['rid'] = service_tuple[1]
    response['sname'] = service_tuple[2]
    response['sdescription'] = service_tuple[3]
    response['sschedule'] = service_tuple[4]

    return response


def _buildServiceByRoomResponse(service_tuple):
    response = {}
    response['sid'] = service_tuple[0]
    response['sname'] = service_tuple[1]
    response['sdescription'] = service_tuple[2]
    response['sschedule'] = service_tuple[3]
    return response


def _buildWebsiteResponse(website_tuple):
    response = {}
    response['wid'] = website_tuple[0]
    response['url'] = website_tuple[1]
    response['wdescription'] = website_tuple[2]

    return response


def _buildCoreWebsiteResponse(website_tuple):
    response = {}
    response['wid'] = website_tuple[0]
    response['wdescription'] = website_tuple[3]
    response['isdeleted'] = website_tuple[2]
    return response


class ServiceHandler:

    def createService(self, json):
        """
        """
       # TODO:SHOULD TAKE PARAMETERS DINAMICALLY CHECKING FOR KEYS
        for key in CREATESERVICEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
       # TODO: NO LIMIT REQUIERED?
        websites = WebsiteHandler().unpackWebsites(json=json['Websites'])
        if len(websites) > 10:
            return jsonify(Error="Improper number of websites provided: " + str(len(websites))), 400
        phones = PhoneHandler().unpackPhones(json=json['PNumbers'])
        if len(websites) > 10:
            return jsonify(Error="Improper number of websites provided: " + str(len(websites))), 400

        # MAKE DICTIONARY TO CRREATE THESE
        user = json['uid']
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
            return jsonify(Error=str(sid)), 400

        return jsonify({"sid": sid}), 201

    def deleteService(self, sid):
        dao = ServiceDAO()
        service = dao.deleteService(sid)
        if service is not None:
            return jsonify(_buildCoreServiceResponse(service))
        return jsonify(Error="No service with that ID"), 404

    def getServiceByID(self, sid, no_json=False):
        """
        Return the Service entry belonging to the specified sid.
        Parameters:
            sid: Service ID.
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing room information. Error JSON otherwise.
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
        dao = ServiceDAO()
        services = dao.getServicesByRoomID(rid=rid)
        serviceInfo = []
        for row in services:
            serviceInfo.append(_buildServiceByRoomResponse(row))
            if no_json:
                return(serviceInfo)
        return jsonify(serviceInfo)

    def getServicesSegmented(self, offset, limit):
        """
        """

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

    def updateServiceInformation(self, sid, json):
        """
        """
        service = {}
        for key in json:
            if key in UPDATESERVICEKEYS:
                service[key] = (json[key])

        dao = ServiceDAO()
        response = _buildServiceResponse(dao.getServiceByID(
            dao.updateServiceInformation(service=service, sid=sid)))
        return jsonify(response)

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

    def getServicesByKeywords(self, json, offset, limit=20):
        """
        Get non-deleted services whose names or descriptions match a search string.
        Parameters:
            json: JSON object with a "searchstring" key.
            offset: Number of result rows to ignore from top of query results.
            limit: Max number of result rows to return. Default=20.
        """

        if not json:
            return jsonify(Error='No JSON Provided.'), 400
        if SEARCHSTRING_VALUE not in json:
            return jsonify(Error='Missing key in JSON: ' + str(SEARCHSTRING_VALUE)), 400
        # TODO: abstract this so multiple handlers can share it.
        keywords = self.processSearchString(
            searchstring=json[SEARCHSTRING_VALUE])
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
