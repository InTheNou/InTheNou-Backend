from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.UserDAO import UserDAO




def _buildUserResponse(user_tuple):
    """
    Private Method to build user dictionary to be JSONified.
    Parameters:
        user_tuple: response tuple from SQL query
    Returns:
        Dict: User information
    """
    response = {}
    response['uid']        = user_tuple[0]
    response['email']      = user_tuple[1]
    response['first_name'] = user_tuple[2]
    response['last_name']  = user_tuple[3]
    response['type']       = user_tuple[4]
    # response['roleid']     = user_tuple[5]

    return response

def _buildDelegatedUserResponse(user_tuple):
    """
    Private Method to build user dictionary to be JSONified.
    Parameters:
        user_tuple: response tuple from SQL query
    Returns:
        Dict: Delegated User information
    """
    response = {}
    
    
  
    response['user_id']       = user_tuple[5]
    response['user_email']    = user_tuple[4]
    response['user_type']     = user_tuple[3]
    response['issuer_email']  = user_tuple[1]
    response['issuer_type']   = user_tuple[0]
    response['issuer_id']      = user_tuple[2]
    return response


class UserHandler:

    def getUserByID(self, uid):
        """Return the user entry belonging to the specified uid.
        uid -- user ID.
        """
        dao = UserDAO()
        user = dao.getUserByID(uid)
        if not user:
            return jsonify(Error='User does not exist: uid=' + str(uid)), 404
        else:
            response = _buildUserResponse(user_tuple=user)
            return jsonify(response)
    

    def getUsersDelegatedByID(self, id):

        dao = UserDAO()
        users =dao.getUsersDelegatedByID(id)
        if not users:
            return jsonify(Error='User does has not delegated any users' + str(id)), 405
        else:
            user_list = []
            for row in users:
                user_list.append(_buildDelegatedUserResponse(user_tuple=row))
            response = {"Users":user_list}
            return jsonify(response)

    def getUsersAndIssuersSegmented(self,offset,limit):

        dao =UserDAO()
        users = dao.getUsersAndIssuersSegmented(offset=offset,limit = limit)
        if not users:
            response = {'users': None}
        else:
            user_list = []
            for row in users:
                user_list.append(_buildDelegatedUserResponse(user_tuple=row))
            response = {"Users":user_list}
            return jsonify(response)

     
    def getUsersSegmented(self,offset,limit):

        dao =UserDAO()
        users = dao.getUsersSegmented(offset=offset,limit = limit)
        if not users:
            response = {'users': None}
        else:
            user_list = []
            for row in users:
                user_list.append(_buildUserResponse(user_tuple=row))
            response = {"Users":user_list}
            return jsonify(response)