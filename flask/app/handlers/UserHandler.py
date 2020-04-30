from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.UserDAO import UserDAO
from flask_login import current_user

CHECKUSERISSUERSKEY = ['id', 'uid']
CHANGEUSERROLEKEY = ['id', 'uid', 'roleid']


def _buildEmailUserResponse(user_tuple):
    """
    Private Method to build user dictionary to be JSONified.
    Parameters:
        :param user_tuple: response tuple from SQL query
    
        :return Dict: User information when given Email
            uid,display name,roleid,the id for role issuer
    """
    response = {}
    response['uid'] = user_tuple[0]
    response['display_name'] = user_tuple[1]
    response['roleid'] = user_tuple[2]
    response['roleissuer'] = user_tuple[3]

    return response


def _buildCoreUserResponse(user_tuple):
    """
    Private Method to build user dictionary to be JSONified.
    Parameters:
        :param user_tuple: response tuple from SQL query
    
        :returns Dict: User information 
            uid,email,display name,roleid,the id for role issuer
    """

    response = {}
    response['uid'] = user_tuple[0]
    response['email'] = user_tuple[1]
    response['display_name'] = user_tuple[2]
    response['type'] = user_tuple[3]
    response['roleid'] = user_tuple[4]

    return response


def _buildUserResponse(user_tuple):
    """
    Private Method to build user dictionary to be JSONified.
    Parameters:
        :param user_tuple: response tuple from SQL query
  
        :returns Dict: User information
    """
    response = {}
    response['uid'] = user_tuple[0]
    response['email'] = user_tuple[1]
    response['display_name'] = user_tuple[2]
    response['roleid'] = user_tuple[3]

    return response


def _buildDelegatedUserResponse(user_tuple):
    """
    Private Method to build user dictionary to be JSONified.
    Parameters:
        :param user_tuple: response tuple from SQL query
    
        :returns Dict: Delegated User information
    """

    response = {}
    response['issuer_role'] = user_tuple[0]
    response['issuer_email'] = user_tuple[1]
    response['issuer_id'] = user_tuple[2]
    response['user_role'] = user_tuple[3]
    response['user_email'] = user_tuple[4]
    response['user_id'] = user_tuple[5]

    return response


def _buildUserNumberResponse(user_tuple):
    """
    Private Method to build user dictionary to be JSONified.

    :param user_tuple: response tuple from SQL query
    :returns Dict: user information with keys:

    .. code-block:: python

        {'number'}
    """
    response = {}

    response['number'] = user_tuple[0]
    return response


def _buildUserIDList(user_tuple):
    """
    Private Method to build user dictionary to be JSONified.

    :param user_tuple: response tuple from SQL query
    :returns Dict: user information with keys:

    .. code-block:: python

        {'user_id'}
    """
    response = {}

    response['user_id'] = user_tuple
    return response


def _checkUser(id, user_tuple):
    """
    Validates user is part of a list.

    :param id: User ID
    :param user_tuple: List of user IDs
    :return: bool
    """

    for row in user_tuple:
        if (int(id) == int(row[0])):
            return True
    return False


class UserHandler:
    # TODO:add No_Json
    def getUserByID(self, uid, no_json=False):
        """Return the user entry belonging to the specified uid.
        uid -- user ID.
        """

        dao = UserDAO()
        if(isinstance(uid, int) and uid > 0):
            user = dao.getUserByID(uid)
        else:
            return jsonify(Error='User does not exist: uid=' + str(uid)), 404

        if not user:
            return jsonify(Error='User does not exist: uid=' + str(uid)), 404
        else:
            if no_json:
                response = _buildCoreUserResponse(user_tuple=user)
                return response
            else:
                response = _buildCoreUserResponse(user_tuple=user)
                return jsonify(response)

    def getUsersThatCanModifyEvent(self, eid, no_json=False):
        """
        Return a list of users that can modify a given event.
        
        


        Uses :func:`~app.DAOs.UserDAO.UserDAO.getUsersThatCanModifyEvent` as well as:

        
         * :func:`~app.handlers.UserHandler.UserHandler._buildUserIDList(`
        
       
        :parameid:Event ID
        :type eid: int
        :param no_json:indicates if this method should respond with a J_son or not 
        :type no_json:bool
        
        
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        dao = UserDAO()
        users = dao.getUsersThatCanModifyEvent(eid=eid)
        if not users:
            response = {'Users': None}
        else:
            user_list = []
            for row in users:
                user_list.append(_buildUserIDList(user_tuple=row))

            response = {"Users": user_list}
            if no_json:
                return response['Users']
            return jsonify(response)

    def getUsersDelegatedByID(self, uid):
        """
        Return a list of users that the given user ID has delegated roles to.
        

        Uses :func:`~app.DAOs.UserDAO.UserDAO.getUsersDelegatedByID` as well as:

        
         * :func:`~app.handlers.UserHandler.UserHandler._buildUserResponse(`
        
       
        :param uid: User ID.
        :type uid: int
        
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        dao = UserDAO()
        users = dao.getUsersDelegatedByID(uid)
        if not users:
            return jsonify(Error='User has not delegated any users UID: ' + str(uid)), 200
        else:
            user_list = []
            for row in users:
                user_list.append(_buildUserResponse(user_tuple=row))
            response = {"Users": user_list}
            return jsonify(response)

    def getUsersAndIssuersSegmented(self, offset, limit):
        """
      
        Return a list of users , segmented.
        Uses :func:`~app.DAOs.UserDAO.UserDAO.getUsersAndIssuersSegmented` as well as:

        
         * :func:`~app.handlers.UserHandler.UserHandler._buildDelegatedUserResponse`
        
       
        :param offset: value of first rows to ignore
        :type offset: int
        :param limit: number of max rows to get from response 
        :type limit: int
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        dao = UserDAO()
        users = dao.getUsersAndIssuersSegmented(offset=offset, limit=limit)
        if not users:
            response = {'Users': None}
        else:
            user_list = []
            for row in users:
                user_list.append(_buildDelegatedUserResponse(user_tuple=row))
            response = {"Users": user_list}
            return jsonify(response)

    def getAllUsersByRoleIDSegmented(self, roleid, offset, limit):
        """
       
        Return a list of users , segmented.
        Uses :func:`~app.DAOs.UserDAO.UserDAO.getAllUsersByRoleID` as well as:

        
         * :func:`~app.handlers.UserHandler.UserHandler._buildCoreUserResponse`
        
        :param roleid: The ID for the role of the users to return
        :param offset: value of first rows to ignore
        :type offset: int
        :param limit: number of max rows to get from response 
        :type limit: int
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        dao = UserDAO()
        users = dao.getAllUsersByRoleID(
            roleid=roleid, offset=offset, limit=limit)
        result = []
        for row in users:
            result.append(_buildCoreUserResponse(row))
        return jsonify(result)

    def getUsersSegmented(self, offset, limit):
        """
        Return a list of users , segmented.
        Uses :func:`~app.DAOs.UserDAO.UserDAO.getUsersSegmented` as well as:

        
         * :func:`~app.handlers.UserHandler.UserHandler._buildCoreUserResponse`
        

        :param offset: value of first rows to ignore
        :type offset: int
        :param limit: number of max rows to get from response 
        :type limit: int
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        dao = UserDAO()
        users = dao.getUsersSegmented(offset=offset, limit=limit)
        if not users:
            response = {'users': None}
        else:
            user_list = []
            for row in users:
                user_list.append(_buildCoreUserResponse(user_tuple=row))
            response = {"Users": user_list}
            return jsonify(response)

    def changeRole(self, uid, id, newRole):
        """
        Attempt to change a user's role id.

        Uses :func:`~app.DAOs.UserDAO.UserDAO.changeRole` as well as:

        
         * :func:`~app.handlers.UserHandler.UserHandler.getUserByID`
         * :func:`~app.handlers.UserHandler.UserHandler.getUserIssuers`
         * :func:`~app.handlers.UserHandler.UserHandler._buildUserResponse`

        :param uid: User ID.
        :type uid: int
        :param id: ID of the User that is making the API call.
        :type id: int
        :param newRole: the new role to assign to a user
        :type newRole: int

        
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """

        userID = uid
        newRole = newRole
        issuer_role = current_user.user_role
        dao = UserDAO()
        userBeingIssued = self.getUserByID(uid=uid, no_json=True)

        oldRole = userBeingIssued['roleid']

        print("old role is "+str(oldRole))

        if int(oldRole) == 1:
            if((newRole <= issuer_role and issuer_role < 4) or issuer_role > 3):
                user = dao.changeRole(id=id, uid=userID, roleid=newRole)
            else:
                return jsonify(Error="User with uid: "+str(id)+" and roleid "+str(current_user.user_role)+" cannot change  role ID "+str(newRole)), 405
        else:
            if self.getUserIssuers(id=id, no_json=True, uid=uid):
                user = dao.changeRole(id=id, uid=userID, roleid=newRole)
            else:
                return jsonify(Error="User with uid: "+str(id)+" and roleid "+str(current_user.user_role)+" cannot change  role ID "+str(newRole)), 405
        if not user:
            return jsonify(Error='Users with roles id does not exist: roleid=' + str(newRole)), 404
        else:
            response = _buildUserResponse(user_tuple=user)
            return jsonify(response)

    def getUserIssuers(self, uid, id, no_json=False):
        """
        Returns a list of users that can be issuers for a given user ID
        Parameters :
        uid: ID of user to get issuers from 
        id: ID of caller
     
       
        Uses :func:`~app.DAOs.UserDAO.UserDAO.getUserIssuers` as well as:

         * :func:`~app.handlers.UserHandler.UserHandler._checkUser`
        
         * :func:`~app.handlers.UserHandler.UserHandler._buildUserIDList`

        :param uid: User ID.
        :type uid: int
        :param id: ID of the User that is making the API call.
        :type id: int
        :param no_json: the new role to assign to a user
        :type no_json: bool

        
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        # for key in CHECKUSERISSUERSKEY:
        #     if key not in json:
        #         return jsonify(Error='Missing credentials from submission: ' + key), 400

        id = id
        userID = uid

        dao = UserDAO()
        users = []
        users = dao.getUserIssuers(userID=userID)
        if not users:
            response = {'Users': None}
            return jsonify(response)

        if no_json:
            return _checkUser(id=id, user_tuple=users)
        else:
            user_list = []
            for row in users:
                user_list.append(_buildUserIDList(user_tuple=row))
            response = user_list

            return jsonify(user_list)

        return jsonify(Error="Error finding user information"), 400

    def getNumberOfUsersByRole(self, roleid):
        """
       Get the number of users with a given role id.

        Uses :func:`~app.DAOs.UserDAO.UserDAO.getNumberOfUsersByRole` as well as:

        
         * :func:`~app.handlers.UserHandler.UserHandler._buildUserNumberResponse`
         

        :param roleid: The ID for the role to look Statistifs for.
        :type roleid: int
       

        
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        dao = UserDAO()
        users = dao.getNumberOfUsersByRole(roleid=roleid)
        if not users:
            return jsonify(Error='Users with roles id does not exist: roleid=' + str(roleid)), 404
        else:
            response = _buildUserNumberResponse(user_tuple=users)
            return jsonify(response)

    def getUserByEmail(self, email):
        """
        Return the user entry belonging to the specified email.
        Uses :func:`~app.DAOs.UserDAO.UserDAO.getUserByEmail` as well as:
         * :func:`~app.handlers.UserHandler.UserHandler._buildEmailUserResponse`
        :param email: the user's email address
        :type email: string
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        

        dao = UserDAO()
        user = dao.getUserByEmail(email=email)
        if not user:
            return jsonify(Error='Users with Email does not exist: email=' + str(email)), 404
        else:
            response = _buildEmailUserResponse(user_tuple=user)
            return jsonify(response)
