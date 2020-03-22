from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.ServiceDAO import ServiceDAO
from app.handlers.RoomHandler import RoomHandler


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
