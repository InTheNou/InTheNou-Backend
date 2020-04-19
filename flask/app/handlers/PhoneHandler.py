from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.PhoneDAO import PhoneDAO
from app.DAOs.ServiceDAO import ServiceDAO
import phonenumbers

PHONETYPEKEYS = ['E', 'L', 'F', 'M']
SERVICEPHONEKEYS = ['PNumbers']


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
            numbers.append(num)
        return numbers

    def insertServicePhone(self, sid, uid, json):
        """
        """

        for key in SERVICEPHONEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
        handler = PhoneHandler()

        phones = []
        phoneInfo = []
        phones = (handler.unpackPhones(json['PNumbers']))
        dao = PhoneDAO()

        if not phones:
            phoneInfo = None
        else:
            for row in phones:

                try:
                    number = phonenumbers.parse(row['pnumber'],"US")
                    if((phonenumbers.is_possible_number(number))):

                        if ((row['ptype']).upper()) in PHONETYPEKEYS:
                            phoneInfo.append((_buildPhoneResponse(dao.getPhoneByID(
                                (dao.addPhoneToService(cursor=None, sid=sid, uid=uid, pid=(dao.insertPhone
                                                                                  (cursor=None, uid=uid, pnumber=row['pnumber'], ptype=row['ptype'].upper()))))[0]))))
                        else:
                            phoneInfo.append(({"pid": None}))
                except:
                    phoneInfo.append(({"pid": None}))

        return jsonify({"PNumbers":(phoneInfo)})

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
            response =  None
        else:
            phone_list = []
            for row in phones:
                phone_list.append(_buildPhoneResponse(phone_tuple=row))
            response = phone_list
        if no_json:
            return response
        return jsonify(response)

    def removePhoneByServiceID(self, sid, json, uid):
        """
        """
        for key in SERVICEPHONEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400

        phones = []
        phoneIDs = []
        phoneInfo = []
        phones = (self.unpackPhones(json['PNumbers']))
        dao = PhoneDAO()

        if not phones:
            phoneInfo = None
        else:
            for x in phones:

                ID = (dao.removePhonesByServiceID(
                    sid=sid, phoneid=x['phoneid'], uid=uid))
                # print('Removed PhoneID '+str(x['phoneid']) + ' from service '+ str(sid))
                if(ID == None):
                    phoneInfo.append("Phone number ID not associated with Service-> sid: " + str(sid) + ' phoneid: ' + (str(x['phoneid'])))
                else:
                    phoneIDs.append((ID))
                # print('Phones deleted IDs: '+ str(phoneIDs))
            for row in phoneIDs:
                phoneInfo.append((_buildPhoneResponse(dao.getPhoneByID(row))))
        return jsonify(phoneInfo)
