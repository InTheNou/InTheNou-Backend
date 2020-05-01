from app import app
from flask import Flask, redirect, url_for, session, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
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

       Uses :func:`~app.handlers.UserHandler.UserHandler.getUserByID`

       Get User By ID

       .. :quickref: User; Get User By by id

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
            "ecreation": "2020-04-25 21:42:57.094493",
            "ecreator": {
                "display_name": "Diego Amador",
                "email": "diego.amador@upr.edu",
                "roleid": 3,
                "type": "Professor",
                "uid": 2
            },
            "edescription": "Meeting to discuss plans for integration phase.",
            "eend": "2020-08-05 17:41:00",
            "eid": 1,
            "estart": "2020-08-05 15:41:00",
            "estatus": "active",
            "estatusdate": "2020-04-25 21:44:00.365692",
            "etitle": "Alpha Code Team Meeting",
            "photourl": "https://images.pexels.com/photos/256541/pexels-photo-256541.jpeg",
            "room": {
                "building": {
                    "babbrev": "S",
                    "bcommonname": "STEFANI",
                    "bid": 1,
                    "bname": "LUIS A STEFANI (INGENIERIA)",
                    "btype": "Academico",
                    "distinctfloors": [1,2,3,4,5,6,7],
                    "numfloors": 7,
                    "photourl": null
                },
                "photourl": null,
                "raltitude": 50.04,
                "rcode": "123A1",
                "rcustodian": "naydag.santiago@upr.edu",
                "rdept": "INGENIERIA ELECTRICA",
                "rdescription": "CAPSTONE",
                "rfloor": 1,
                "rid": 56,
                "rlatitude": 50.04,
                "rlongitude": 50.04,
                "roccupancy": 0
            },
            "tags": [
                {"tid": 6,"tname": "ARTE"},
                {"tid": 42,"tname": "FILO"},
                {"tid": 54,"tname": "ICOM"},
                {"tid": 64,"tname": "INSO"}
            ],
            "websites": [
                {
                    "url": "http://ece.uprm.edu/~fvega/",
                    "wdescription": "Our clients webpage",
                    "wid": 2
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
        return UserHandler().getUserByID(uid=uid)

    else:
        return jsonify(Error='Method not allowed.'), 405

@app.route("/API/App/Users/canModify/eid=<int:eid>", methods=['GET'])
@user_role_required
def getUsersThatCanModifyEvent(eid):
    if request.method == 'GET':
        return UserHandler().getUsersThatCanModifyEvent(eid=eid)
    else:
        return jsonify(Error='Method not allowed.'), 405

@app.route("/API/Dashboard/Users/email=<string:email>", methods=['GET'])
@mod_role_required
def getUserByEmail(email):
    if request.method == 'GET':
        return UserHandler().getUserByEmail(email=email)

    else:
        return jsonify(Error='Method not allowed.'), 405

##DASHBOARD ROUTES##

@app.route("/API/Dashboard/Users/uid=<int:uid>/changeRole/roleid=<int:roleid>", methods=['POST'])
@mod_role_required
def changeRole(uid,roleid):
    if request.method == 'POST':
        return UserHandler().changeRole(newRole=roleid,uid=uid,id=current_user.id)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route("/API/Dashboard/Users/uid=<int:uid>/Delegated", methods=['GET'])
@mod_role_required
def getDelegatedUserByID(uid):
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
    if request.method == 'GET':
        return UserHandler().getUsersAndIssuersSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error='Method not allowed.'), 405


@app.route("/API/Dashboard/Users/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@admin_role_required
def geUsersSegmented(offset, limit):
    if request.method == 'GET':
        return UserHandler().getUsersSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error='Method not allowed.'), 405


@app.route("/API/Dashboard/Users/roleid=<int:roleid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@admin_role_required
def getAllUsersByRoleID(roleid, offset, limit):
    if request.method == 'GET':
        return UserHandler().getAllUsersByRoleIDSegmented(roleid=roleid, offset=offset, limit=limit)
    else:
        return jsonify(Error='Method not allowed.'), 405


@app.route("/API/Dashboard/Stats/roleid=<int:roleid>", methods=['GET'])
@admin_role_required
def geNumberOdUsersByRole(roleid):
    if request.method == 'GET':
        return UserHandler().getNumberOfUsersByRole(roleid=roleid)
    else:
        return jsonify(Error='Method not allowed.'), 405
