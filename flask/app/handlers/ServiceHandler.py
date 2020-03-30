from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.ServiceDAO import ServiceDAO
from app.handlers.RoomHandler import RoomHandler

SEARCHSTRING_VALUE = 'searchstring'

def _buildPhoneResponse(phone_tuple):
    response = {}
    response['phoneid'] = phone_tuple[0]
    response['pnumber'] = phone_tuple[1]
    response['ptype'] = phone_tuple[2]
    response['isdeleted'] = phone_tuple[3]
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


def _buildWebsiteResponse(website_tuple):
    response = {}
    response['wid'] = website_tuple[0]
    response['url'] = website_tuple[1]
    response['wdescription'] = website_tuple[2]
    response['isdeleted'] = website_tuple[3]
    return response


class ServiceHandler:

    def getServiceByID(self, sid, no_json=False):
        """
        Return the Service entry belonging to the specified sid.
        Parameters:
            sid: Service ID.
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing room information. Error JSON otherwise.
        """
        dao = ServiceDAO()
        service = dao.getServiceByID(sid=sid)
        if not service:
            return jsonify(Error='Service does not exist: sid=' + str(sid)), 404
        else:
            response = _buildServiceResponse(service_tuple=service)
            response["phones"] = self.getServicePhones(sid=sid, no_json=True)['phones']
            response["websites"] = self.getServiceWebsites(sid=sid, no_json=True)['websites']
            if no_json:
                return response
            return jsonify(response)

    def getServicePhones(self, sid, no_json=False):
        """
            Return the Phone entries belonging to the specified Service sid.
            Parameters:
                sid: Service ID.
                no_json: states if the response should be returned as JSON or not.
            Returns:
                JSON: containing room information. Error JSON otherwise.
            """
        dao = ServiceDAO()
        phones = dao.getServicePhones(sid=sid)
        if not phones:
            response = {"phones": None}
        else:
            phone_list = []
            for row in phones:
                phone_list.append(_buildPhoneResponse(phone_tuple=row))
            response = {"phones": phone_list}
        if no_json:
            return response
        return jsonify(response)

    def getServiceWebsites(self, sid, no_json=False):
        """
            Return the Website entries belonging to the specified Service sid.
            Parameters:
                sid: Service ID.
                no_json: states if the response should be returned as JSON or not.
            Returns:
                JSON: containing room information. Error JSON otherwise.
            """
        dao = ServiceDAO()
        websites = dao.getServiceWebsites(sid=sid)
        if not websites:
            response = {"websites": None}
        else:
            website_list = []
            for row in websites:
                website_list.append(_buildWebsiteResponse(website_tuple=row))
            response = {"websites": website_list}
        if no_json:
            return response
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
            return jsonify(Error='No JSON Provided.'), 401
        if SEARCHSTRING_VALUE not in json:
            return jsonify(Error='Missing key in JSON: ' + str(SEARCHSTRING_VALUE)), 401
        # TODO: abstract this so multiple handlers can share it.
        keywords = self.processSearchString(searchstring=json[SEARCHSTRING_VALUE])
        dao = ServiceDAO()
        services = dao.getServicesByKeywords(searchstring=keywords, offset=offset, limit=limit)
        if not services:
            response = {'services': None}
        else:
            service_list=[]
            for row in services:
                service_list.append(_buildServiceResponse(service_tuple=row))
            response = {'services': service_list}
        return jsonify(response)
