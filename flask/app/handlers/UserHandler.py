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
    response['roleid']     = user_tuple[5]

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
