from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.PhoneDAO import PhoneDAO
from app.DAOs.ServiceDAO import ServiceDAO


SERVICEPHONEKEYS=['PNumbers']

def _buildPhoneResponse(phone_tuple):
    response = {}
    response['phoneid'] = phone_tuple[0]
    response['pnumber'] = phone_tuple[1]
    response['ptype'] = phone_tuple[2]
    
    return response




class PhoneHandler:

    def unpackPhones(self, json):
        numbers = []
        for num in json:
            numbers.append(num['number'])
        return numbers

    def insertServicePhone(self,sid,json):
        """
        """ 
        for key in SERVICEPHONEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
        handler =PhoneHandler()

        
        phones=[]
        phoneInfo= []
        phones= (handler.unpackPhones(json['PNumbers']))
        dao =PhoneDAO()
       
       
        if not phones:
            phoneInfo = None
        else:
            for row in phones:
                phoneInfo.append(( _buildPhoneResponse (dao.getPhoneByID(
                  (dao.addPhoneToService(cursor=None,sid=sid,pid=(dao.insertPhone
                  (cursor=None, pnumber=row['pnumber'],ptype=row['ptype'])))))))
                )

        return jsonify(phoneInfo)
    
    def getPhonesByServiceID(self, sid, no_json=False):
        """
        Return the Phone entries belonging to the specified Service sid.
        Parameters:
            sid: Service ID.
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing room information. Error JSON otherwise.
        """
        dao = PhoneDAO()
        phones = dao.getPhonesByServiceID(sid=sid)
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

    def removePhoneByServiceID(self,sid,json):
        """
        """ 
        for key in SERVICEPHONEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400 
        
        phones    = []
        phoneIDs =  []
        phoneInfo = []
        phones    = (self.unpackPhones(json['PNumbers']))
        dao       = PhoneDAO()
        
        if not phones:
            phoneInfo = None
        else:
            
            for x in phones:
                    
                ID=(dao.removePhonesByServiceID(sid=sid, phoneid=x['phoneid']))
                    #print('Removed PhoneID '+str(x['phoneid']) + ' from service '+ str(sid))
                if(ID == None):
                    return jsonify(Error="Phone number ID not associated with Service-> sid: " + str(sid) + ' phoneid: '+ (str(x['phoneid']))), 400
                phoneIDs.append(int(ID))
                    #print('Phones deleted IDs: '+ str(phoneIDs))
            for row in phoneIDs:
                phoneInfo.append(( _buildPhoneResponse(dao.getPhoneByID(row)) )) 
        return jsonify(phoneInfo) 
        
        