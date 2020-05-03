from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.PhoneDAO import PhoneDAO
from app.DAOs.ServiceDAO import ServiceDAO
import phonenumbers

PHONETYPEKEYS = ['E', 'L', 'F', 'M']
SERVICEPHONEKEYS = ['PNumbers']


def _buildPhoneResponse(phone_tuple):
    """
    Private Method to build phone number dictionary to be JSONified.

    :param: phone_tuple: response tuple from SQL query
    :returns Dict: Phone information with keys:

    .. code-block:: python

        {'phoneid', 'pnumber', 'ptype'}
    """
    response = {}
    response['phoneid'] = phone_tuple[0]
    response['pnumber'] = phone_tuple[1]
    response['ptype'] = phone_tuple[2]

    return response


class PhoneHandler:
    """
    Handler Class to manage getting/creating/modifying phones
    """

    def unpackPhones(self, json):
        """
        Returns a lsit of phone numbers given a json body with phone numbers and types 

        :param json: JSON payload with phone numbers
        :type json: array
        :return list: list of numbers
        """
        numbers = []
        for num in json:
            numbers.append(num)
        return numbers

    def insertServicePhone(self, sid, uid, json):
        """
        Create a phone number and add it to a service given its ID.

        Uses :func:`~app.DAOs.PhoneDAO.PhoneDAO.insertPhones` as well
        as :func:`~app.handlers.PhoneHandler.PhoneHandler.unpackPhones`


        :param sid: The ID of the service to add phone numbers to
        :type sid: int
        :param uid: User ID.
        :type uid: int
        :param json: JSON containing the phone numbers to add
        :type json: array
        :return: result from :func:`~app.DAOs.PhoneDAO.PhoneDAO.insertPhones`
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
            phoneInfo = dao.insertPhones(phones, sid, uid=uid)

        return phoneInfo

    def getPhonesByServiceID(self, sid, no_json=False):
        """
        Create a phone number and add it to a service given its ID 

        Uses :func:`~app.DAOs.PhoneDAO.PhoneDAO.getPhonesByServiceID`
        as well as :func:`~app.handlers.PhoneHandler._buildPhoneResponse`

        :param sid: The ID of the service to add phone numbers to
        :type sid: int
        :param no_json: Specify if response is Json or not
        :type no_json: bool
        :return JSON: list of phones
        """
        dao = PhoneDAO()
        phones = dao.getPhonesByServiceID(sid=sid)
        if not phones:
            response = None
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
        Remove a phone number from a service given its ID

        Uses:

            * :func:`~app.DAOs.PhoneDAO.PhoneDAO.removePhonesByServiceID`
            * :func:`~app.handlers.PhoneHandler._buildPhoneResponse`
            * :func:`~app.handlers.PhoneHandler.PhoneHandler.unpackPhones`

        :param sid: The ID of the service to add phone numbers to
        :type sid: int
        :param uid: User ID.
        :type uid: int
        :param json: JSON containing the phone numbers to add
        :type json: array
        :return JSON: phone number information.
        """
        for key in SERVICEPHONEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
        print("sending pids")
        phoneIDs = []
        phoneInfo = []
        phones = (self.unpackPhones(json['PNumbers']))
        dao = PhoneDAO()
        if not phones:
            phoneInfo = None
        else:
            for x in phones:
                if x['phoneid'] != "":
                    ID = dao.removePhonesByServiceID(sid=sid, phoneid=x['phoneid'], uid=uid)
                    if ID is None:
                        phoneInfo.append("Phone number ID not associated with Service-> sid: "
                                         + str(sid) + ' phoneid: ' + str(x['phoneid']))
                    else:
                        phoneIDs.append(ID)
                else:
                    phoneInfo.append("Phone number ID not associated with Service-> sid: "
                                     + str(sid) + ' phoneid: ' + str(x['phoneid']))
            for row in phoneIDs:
                phoneInfo.append(_buildPhoneResponse(dao.getPhoneByID(row)))
        return jsonify(phoneInfo)
