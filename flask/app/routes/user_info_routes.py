from app import app
from flask import Flask, redirect, url_for, session, jsonify, request
from flask_dance.contrib.google import make_google_blueprint
from app.handlers.UserHandler import UserHandler
from flask_login import login_required, logout_user, current_user
from app.oauth import admin_role_required, mod_role_required,user_role_required


@app.errorhandler(404)
def not_found(Error):
    """Page not found."""
    return jsonify(Error='NOT FOUND'), 404
##APP ROUTES##

@app.route("/API/App/Users/uid=<int:uid>", methods=['GET'])
@user_role_required
def getUserByID(uid):
    """
    .. py:decorator:: user_role_required
    .. :quickref: User; Get User By by id
    
    User; Get User By ID
    Uses :func:`~app.handlers.UserHandler.UserHandler.getUserByID`

    
    :param uid: User ID
    :type uid: int
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        GET /API/App/Users/uid=1 HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
            "display_name": "Brian Rodriguez",
            "email": "brianrodrig@gmail.com",
            "roleid": 4,
            "type": "Student",
            "uid": 1
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 404: User does not exist
    """
    if request.method == 'GET':
        return UserHandler().getUserByID(uid=uid)

    else:
        return jsonify(Error='Method not allowed.'), 405

@app.route("/API/App/Users/canModify/eid=<int:eid>", methods=['GET'])
@admin_role_required
def getUsersThatCanModifyEvent(eid):
    """
    .. py:decorator:: admin_role_required
    .. :quickref: User; Get Users that can modify a given event
    
    Get Users that can modify an event
    Uses :func:`~app.handlers.UserHandler.UserHandler.getUserThatCanModifyEvent`

    
    :param eid: event ID
    :type eid: int
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        GET /API/App/Users/canModify/eid=1 HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
            "users": [
                {
                    "user_id": [
                        1
                    ]
                },
                {
                    "user_id": [
                        2
                    ]
                },
                {
                    "user_id": [
                        11
                    ]
                }
            ]
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 404: Event does not exist
    """
    
    if request.method == 'GET':
        return UserHandler().getUsersThatCanModifyEvent(eid=eid)
    else:
        return jsonify(Error='Method not allowed.'), 405

@app.route("/API/Dashboard/Users/email=<string:email>", methods=['GET'])
@mod_role_required
def getUserByEmail(email):
    """
    .. py:decorator:: user_role_required
    .. :quickref: User; Get User by email
    
    Get User given an email
    Uses :func:`~app.handlers.UserHandler.UserHandler.getUserByEmail`

    
    :param email: User email
    :type email: string
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        GET /API/Dashboard/Users/email=jonathan.santiago27@upr.edu HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
            "display_name": "Jonathan X Santiago Gonzalez",
            "roleid": 4,
            "roleissuer": 1,
            "uid": 11
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 404: Email does not exist
    """
    if request.method == 'GET':
        return UserHandler().getUserByEmail(email=email)

    else:
        return jsonify(Error='Method not allowed.'), 405

##DASHBOARD ROUTES##

@app.route("/API/Dashboard/Users/uid=<int:uid>/changeRole/roleid=<int:roleid>", methods=['POST'])
@mod_role_required
def changeRole(uid,roleid):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: User; Change User Role
    
    Change user role
    Uses :func:`~app.handlers.UserHandler.UserHandler.changeRole`

    
    :param uid: User ID
    :type uid: int
    :param roleid: User role ID
    :type roleid: int
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        GET /API/Dashboard/Users/uid=5/changeRole/roleid=1 HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
            "display_name": "Sofia Saavedra",
            "email": "sofia.saavedra@upr.edu",
            "roleid": 1,
            "uid": 5
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 404: User does not exist
    """
    if request.method == 'POST':
        return UserHandler().changeRole(newRole=roleid,uid=uid,id=current_user.id)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route("/API/Dashboard/Users/uid=<int:uid>/Delegated", methods=['GET'])
@mod_role_required
def getDelegatedUserByID(uid):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: User; Get delegated users
    
    Get delegated users
    Uses :func:`~app.handlers.UserHandler.UserHandler.getUsersDelegatedByID`

    
    :param uid: User ID
    :type uid: int
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        GET /API/Dashboard/Users/uid=11/Delegated HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
           "users": [
               {
                   "display_name": "Sofia Saavedra",
                   "email": "sofia.saavedra@upr.edu",
                   "roleid": 1,
                   "uid": 5
               }
           ]
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 404: User does not exist
    """
    if request.method == 'GET':
            if(current_user.id == uid ):
                return UserHandler().getUsersDelegatedByID(uid=int(current_user.id))
            else:
                print(current_user.user_role)
                if int(current_user.user_role) > 3:
                    return UserHandler().getUsersDelegatedByID(uid=int(uid))
                else:
                    return jsonify(Error='Method not allowed for user role'), 401    
    else:
        return jsonify(Error='Method not allowed.'), 405

@app.route("/API/Dashboard/Users/Permissions/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@admin_role_required
def geUsersAndIssuersSegmented(offset, limit):
    """
    .. py:decorator:: admin_role_required
    .. :quickref: User; Get Users and issuers
    
    Get users and delegators
    Uses :func:`~app.handlers.UserHandler.UserHandler.getUsersAndIssuersSegmented`

    
  
    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        GET /API/Dashboard/Users/Permissions/offset=0/limit=5 HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
            "users": 
            [
                {
                    "issuer_email": "brianrodrig@gmail.com",
                    "issuer_id": 1,
                    "issuer_role": "Admin",
                    "user_email": "diego.amador@upr.edu",
                    "user_id": 2,
                    "user_role": "Moderator"
                },
                {
                    "issuer_email": "diego.amador@upr.edu",
                    "issuer_id": 2,
                    "issuer_role": "Moderator",
                    "user_email": "kensy.bernadeau@upr.edu",
                    "user_id": 3,
                    "user_role": "Event_Creator"
                },
                {
                    "issuer_email": "brianrodrig@gmail.com",
                    "issuer_id": 1,
                    "issuer_role": "Admin",
                    "user_email": "jon123123123athan01228@gmail.com",
                    "user_id": 7,
                    "user_role": "User"
                },
                {
                    "issuer_email": "22222jonathan.santiago27@upr.edu",
                    "issuer_id": 4,
                    "issuer_role": "User",
                    "user_email": "brianrodrig@gmail.com",
                    "user_id": 1,
                    "user_role": "Admin"
                },
                {
                    "issuer_email": "brianrodrig@gmail.com",
                    "issuer_id": 1,
                    "issuer_role": "Admin",
                    "user_email": "22222jonathan.santiago27@upr.edu",
                    "user_id": 4,
                    "user_role": "User"
                }
            ]
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return UserHandler().getUsersAndIssuersSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error='Method not allowed.'), 405


@app.route("/API/Dashboard/Users/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@admin_role_required
def geUsersSegmented(offset, limit):
    """
    .. py:decorator:: admin_role_required
    .. :quickref: User; Get all users,segmented
    
    Get users,segmented
    Uses :func:`~app.handlers.UserHandler.UserHandler.getUsersSegmented`

    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        GET /API/Dashboard/Users/offset=0/limit=5 HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
            "users": 
            [
                {
                    "display_name": "Sofia Saavedra",
                    "email": "sofia.saavedra@upr.edu",
                    "roleid": 1,
                    "type": "User",
                    "uid": 5
                },
                {
                    "display_name": "jonathan santiago",
                    "email": "jonathan01228@gmail.com",
                    "roleid": 1,
                    "type": "User",
                    "uid": 10
                },
                {
                    "display_name": "jonathan santiago",
                    "email": "jonathan011111228@gmail.com",
                    "roleid": 1,
                    "type": "User",
                    "uid": 9
                },
                {
                    "display_name": "jonathan santiago",
                    "email": "111jonathan01228@gmail.com",
                    "roleid": 1,
                    "type": "User",
                    "uid": 8
                },
                {
                    "display_name": "Jonathan Santiago",
                    "email": "22222jonathan.santiago27@upr.edu",
                    "roleid": 1,
                    "type": "User",
                    "uid": 4
                }
            ]
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    """
    if request.method == 'GET':
        return UserHandler().getUsersSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error='Method not allowed.'), 405


@app.route("/API/Dashboard/Users/roleid=<int:roleid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@admin_role_required
def getAllUsersByRoleID(roleid, offset, limit):
    """
    .. py:decorator:: admin_role_required
    .. :quickref: User; Get all users by role id, segmented
    
    Get users by role id, segmented
    Uses :func:`~app.handlers.UserHandler.UserHandler.getAllUsersByRoleIDSegmented`

    :param roleid: User role ID
    :type roleid: int
    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        GET /API/Dashboard/Users/roleid=1/offset=0/limit=5 HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
            "users": 
            [
                {
                    "display_name": "jonathan santiago",
                    "email": "jon123123123athan01228@gmail.com",
                    "roleid": 1,
                    "type": "User",
                    "uid": 7
                },
                {
                    "display_name": "Jonathan Santiago",
                    "email": "22222jonathan.santiago27@upr.edu",
                    "roleid": 1,
                    "type": "User",
                    "uid": 4
                },
                {
                    "display_name": "jonathan santiago",
                    "email": "111jonathan01228@gmail.com",
                    "roleid": 1,
                    "type": "User",
                    "uid": 8
                },
                {
                    "display_name": "jonathan santiago",
                    "email": "jonathan011111228@gmail.com",
                    "roleid": 1,
                    "type": "User",
                    "uid": 9
                },
                {
                    "display_name": "jonathan santiago",
                    "email": "jonathan01228@gmail.com",
                    "roleid": 1,
                    "type": "User",
                    "uid": 10
                }
            ]
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    """
    if request.method == 'GET':
        return UserHandler().getAllUsersByRoleIDSegmented(roleid=roleid, offset=offset, limit=limit)
    else:
        return jsonify(Error='Method not allowed.'), 405


@app.route("/API/Dashboard/Stats/roleid=<int:roleid>", methods=['GET'])
@admin_role_required
def geNumberOdUsersByRole(roleid):
    """
    .. py:decorator:: admin_role_required
    .. :quickref: User; get Number of users by roleid
    
    Get number of users by role id
    Uses :func:`~app.handlers.UserHandler.UserHandler.getNumberOfUsersByRole`

    :param roleid: User role ID
    :type roleid: int
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        GET /API/Dashboard/Stats/roleid=1 HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
            "number": 6
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 404: roleid not found
    """
    if request.method == 'GET':
        return UserHandler().getNumberOfUsersByRole(roleid=roleid)
    else:
        return jsonify(Error='Method not allowed.'), 405
