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

@app.route("/Dashboard/Users/email=<string:email>", methods=['GET'])
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
