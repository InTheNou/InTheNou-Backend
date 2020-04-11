from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.UserDAO import UserDAO


CHECKUSERISSUERSKEY = ['id', 'uid']
CHANGEUSERROLEKEY = ['id', 'uid', 'roleid']

def _buildEmailUserResponse(user_tuple):
    """
    Private Method to build user dictionary to be JSONified.
    Parameters:
        user_tuple: response tuple from SQL query
    Returns:
        Dict: User information when given Email
            uid,display name,roleid,the id for role issuer
    """
    response = {}
    response['uid'] = user_tuple[0]
    response['display_name'] = user_tuple[1]
    response['roleid']= user_tuple[2]
    response['roleissuer']= user_tuple[3]
      
    return response

def _buildCoreUserResponse(user_tuple):
    """
    Private Method to build user dictionary to be JSONified.
    Parameters:
        user_tuple: response tuple from SQL query
    Returns:
        Dict: User information 
            uid,email,display name,roleid,the id for role issuer
    """
    response = {}
    response['uid'] = user_tuple[0]
    response['email'] = user_tuple[1]
    response['display_name'] = user_tuple[2]
    response['type']    =user_tuple[3]
    response['roleid']  =user_tuple[4]
    
    return response


def _buildUserResponse(user_tuple):
    """
    Private Method to build user dictionary to be JSONified.
    Parameters:
        user_tuple: response tuple from SQL query
    Returns:
        Dict: User information
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
        user_tuple: response tuple from SQL query
    Returns:
        Dict: Delegated User information
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
    Return the amount of users with a given roleid
    roleid -- Role ID
    """
    response = {}

    response['number'] = user_tuple[0]
    return response


def _buildUserIDList(user_tuple):
    """
    Return a list of users with their ID
    user_id -- User ID
    """
    response = {}

    response['user_id'] = user_tuple[0]
    return response


def _checkUser(id, user_tuple):
    """
    Checks if a given id is in a list of user iDs
    id- User ID to check
    """
    for row in user_tuple:
        print(row)
        if (int(id) == int((row['user_id']))):
            return True
    return False


class UserHandler:
    # TODO:add No_Json
    def getUserByID(self, uid, no_json=False):
        """Return the user entry belonging to the specified uid.
        uid -- user ID.
        """
        print(uid)
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
        """Return a list of users that can modify a given event.
        eid:Event ID
        no_json:indicates if this method should respond with a J_son or not 

        """
        dao = UserDAO()
        users = dao.getUsersThatCanModifyEvent(eid=eid)
        if not users:
            response = {'users': None}
        else:
            user_list = []
            for row in users:
                user_list.append(_buildUserIDList(user_tuple=row))
            response = {"Users": user_list}
            if no_json:
                return response
            return jsonify(response)

    def getUsersDelegatedByID(self,uid):
        """
        Return a list of users that the given user ID has delegated roles to.
        id -- user ID.
        uid-- id to look for in the system
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
        Return a list of users and who gave them their roles, segmented.
        offset: value of first rows to ignore
        limit: number of max rows to get from response 

        """
        dao = UserDAO()
        users = dao.getUsersAndIssuersSegmented(offset=offset, limit=limit)
        if not users:
            response = {'users': None}
        else:
            user_list = []
            for row in users:
                user_list.append(_buildDelegatedUserResponse(user_tuple=row))
            response = {"Users": user_list}
            return jsonify(response)

    def getAllUsersByRoleIDSegmented(self, roleid, offset, limit):
        """
        Return a list of users who have given roleid , segmented.
        Parameters:
        roleid: number representing what role type of users to get 
        offset: value of first rows to ignore
        limit: number of max rows to get from response 
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
        Parameters:
        offset: value of first rows to ignore
        limit: number of max rows to get from response 

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

    def changeRole(self, json):
        """
        Update user role id after checking if caller has permissions 
        Parameters : 
        uid: ID of user to change roles
        roleid:new role to assign
        id:uid of caller also called Issuer

        Returns: User entry with new values
        """
        for key in CHANGEUSERROLEKEY:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400

        id = json['id']
        userID = json['uid']
        newRole = json['roleid']

        dao = UserDAO()
        user = dao.changeRole(id=id, uid=userID, roleid=newRole)
        if not user:
            return jsonify(Error='Users with roles id does not exist: roleid=' + str(newRole)), 404
        else:
            response = _buildUserResponse(user_tuple=user)
            return jsonify(response)

    # TODO:MAKE THIS ROUTE SEGMENTED?
    def getUserIssuers(self, json, no_json=False):
        """
        Returns a list of users that can be issuers for a given user ID
        Parameters :
        uid: ID of user to get issuers from 
        id: ID of caller
        roleid: new role to assign
        """
        for key in CHECKUSERISSUERSKEY:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400

        id = json['id']
        userID = json['uid']
        newRole = json['roleid']
        dao = UserDAO()
        users = []
        users = dao.getUserIssuers(userID=userID, newRole=newRole)
        if not users:
            response = {'users': None}
        else:
            user_list = []
            for row in users:
                user_list.append(_buildUserIDList(user_tuple=row))
            response = user_list
        if no_json:
            return _checkUser(id=id, user_tuple=response)
        else:
            return jsonify(user_list)

        return jsonify(Error="Error finding user information"), 400

    def getNumberOfUsersByRole(self, roleid):
        """
        Returns a number of users with a given role
        parameters:
        roleid: Role ID
        """
        dao = UserDAO()
        users = dao.getNumberOfUsersByRole(roleid=roleid)
        if not users:
            return jsonify(Error='Users with roles id does not exist: roleid=' + str(roleid)), 404
        else:
            response = _buildUserNumberResponse(user_tuple=users)
            return jsonify(response)

    def getUserByEmail(self,email):
        """
        Return the user entry belonging to the specified email.
        Parameter:
        email: the user's email address
        """

        dao=UserDAO()
        user = dao.getUserByEmail(email=email)
        if not user:
            return jsonify(Error='Users with Email does not exist: email=' + str(email)), 404
        else:
            response = _buildEmailUserResponse(user_tuple=user)
            return jsonify(response)
