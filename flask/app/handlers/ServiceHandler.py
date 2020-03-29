from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.ServiceDAO import ServiceDAO
from app.DAOs.WebsiteDAO import WebsiteDAO
from app.DAOs.PhoneDAO import PhoneDAO
from app.handlers.RoomHandler import RoomHandler
from app.handlers.WebsiteHandler import WebsiteHandler
from app.handlers.PhoneHandler import PhoneHandler


CREATESERVICEKEYS   =   ['uid','rid','sname','sdescription','sschedule','PNumbers','Websites']
UPDATESERVICEKEYS   =   ['sname','sdescription','sschedule','rid']



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
  
    def createService(self,json):
        """
        """
       
        for key in CREATESERVICEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
       
        websites = WebsiteHandler().unpackWebsites(json=json['Websites'])
        if len(websites) < 1 or len(websites) > 10:
            return jsonify(Error="Improper number of websites provided: "+ str(len(websites))), 400
        # TODO: pass uid not through json

        phones=PhoneHandler().unpackPhones(json=json['PNumbers'])
        if len(phones) < 1 or len(websites) > 10:
            return jsonify(Error="Improper number of websites provided: "+ str(len(websites))), 400


        user=json['uid']
        roomID =json['rid']
        name =json['sname']
        description = json['sdescription']
        schedule=json['sschedule']
        
        dao = ServiceDAO()
        service =dao.createService(uid=user,
                                rid=roomID,
                                sname=name,
                                sdescription=description,
                                sschedule=schedule,
                                isdeleted=False,
                                websites=websites,
                                numbers = phones
                                )
        try:
            sid = service[0]
        except TypeError:
            return jsonify(Error=str(sid)), 400

        return jsonify({"sid": sid}), 201


    def getServiceByID(self, sid, no_json=False):
        """
        Return the Service entry belonging to the specified sid.
        Parameters:
            sid: Service ID.
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing room information. Error JSON otherwise.
        """
        Phonehandler= PhoneHandler()
        Websitehandler= WebsiteHandler()
        dao=ServiceDAO()
        service = dao.getServiceByID(sid=sid)
        if not service:
            return jsonify(Error='Service does not exist: sid=' + str(sid)), 404
        else:
            response = _buildServiceResponse(service_tuple=service)
            response['PNumbers']= Phonehandler.getPhonesByServiceID(sid=sid, no_json=True)['phones']
            response['Websites']= Websitehandler.getWebistesByServiceID( sid=sid, no_json=True )['Websites']
            if no_json:
                return response
            return jsonify(response)

    def getServicesSegmented(self,offset,limit):
        """
        """
        
        dao=ServiceDAO()
        
        services = dao.getServicesSegmented(offset=offset,limit=limit)
        if not services:
            response = {'Services':None}
        else:
            service_list=[]
            for row in services:
                service_list.append(_buildServiceResponse(row))
            response={'Services':service_list}
            return jsonify(response)


    def updateServiceInformation(self,sid,json):
        """
        """
        service ={}
        for key in json:
            if key  in UPDATESERVICEKEYS:
                service[key]=(json[key])  
    
        dao=ServiceDAO()
        response = _buildServiceResponse(dao.getServiceByID(dao.updateServiceInformation(service=service,sid=sid)))
        return jsonify(response) 