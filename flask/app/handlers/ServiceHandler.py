from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.ServiceDAO import ServiceDAO
from app.DAOs.WebsiteDAO import WebsiteDAO
from app.handlers.RoomHandler import RoomHandler
from app.handlers.WebsiteHandler import WebsiteHandler
from app.handlers.PhoneHandler import PhoneHandler


CREATESERVICEKEYS =['uid','rid','sname','sdescription','sschedule','PNumbers','Websites']
DELETESERVICEWEBSITEKEYS = ['sid','wid']
INSERTSERVICEWEBSITEKEYS =['Websites']

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

    def removeServiceWebsite(self,json):
        """
        """ 
        for key in DELETESERVICEWEBSITEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
        print(json)
        sid=json['sid']
        wid=json['wid']
        
        dao =WebsiteDAO()
        website = dao.removeServiceWebsite(wid=wid,sid=sid)
        handler =WebsiteHandler()
        website=handler.getWebsiteByID(wid=website[0])
        return website


    def insertServiceWebsite(self,sid,json):
        """
        """ 
        for key in INSERTSERVICEWEBSITEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
        handler =WebsiteHandler()

        
        sites=[]
        website= []
        sites= (handler.unpackWebsites(json['Websites']))
        dao =WebsiteDAO()
       
        
        if not sites:
            website = None
        else:
            for row in sites:
              website.append(dao.insertWebsiteToService(sid=sid,wid=(dao.createWebsite(url=row['url'])),wdescription=row['wdescription']))

        return website




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
        dao = ServiceDAO()
        service = dao.getServiceByID(sid=sid)
        if not service:
            return jsonify(Error='Service does not exist: sid=' + str(sid)), 404
        else:
            response = _buildServiceResponse(service_tuple=service)
            response["phones"] = self.getServicePhones(sid=sid, no_json=True)['phones']
            response["websites"] = self.getServiceWebsite(sid=sid, no_json=True)['websites']
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

    def getServiceWebsite(self, sid, no_json=False):
        """
            Return the Website entries belonging to the specified Service sid.
            Parameters:
                sid: Service ID.
                no_json: states if the response should be returned as JSON or not.
            Returns:
                JSON: containing room information. Error JSON otherwise.
            """
        dao = WebsiteDAO()
        websites = dao.getWebsitesByServiceID(sid=sid)
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
