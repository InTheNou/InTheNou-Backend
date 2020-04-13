from app import app
from flask import Flask, redirect, url_for, session, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from app.handlers.UserHandler import UserHandler
from flask_login import login_required, logout_user, current_user
from app.oauth import admin_role_required, mod_role_required


@app.errorhandler(404)
def not_found(Error):
    """Page not found."""
    return jsonify(Error='NOT FOUND'), 404
##APP ROUTES##


@app.route("/App/Users/uid=<int:uid>", methods=['GET'])
# @login_required
# @mod_role_required
def getUserByID(uid):
    if request.method == 'GET':
        return UserHandler().getUserByID(uid=uid)

    else:
        return jsonify(Error='Method not allowed.'), 405


@app.route("/App/Users/canModify/eid=<int:eid>", methods=['GET'])
def getUsersThatCanModifyEvent(eid):
    if request.method == 'GET':
        return UserHandler().getUsersThatCanModifyEvent(eid=eid)
    else:
        return jsonify(Error='Method not allowed.'), 405

@app.route("/App/Users/email=<string:email>", methods=['GET'])
# @login_required
# @mod_role_required
def getUserByEmail(email):
    if request.method == 'GET':
        return UserHandler().getUserByEmail(email=email)

    else:
        return jsonify(Error='Method not allowed.'), 405



##DASHBOARD ROUTES##
# TODO: verify the user has event creator + privileges
# TODO: Pass uid from session.

# TEST ROUTE #
# @app.route("/Dashboard/Users/getUserIssuers", methods=['GET'])
# def getUserIssuers():
#         if request.method == 'GET':
#             return UserHandler().getUserIssuers(json =request.json)
#         else: return jsonify(Error="User cannot change  role ID"), 405


@app.route("/Dashboard/Users/changeRole", methods=['POST'])
@mod_role_required
def changeRole():
    if request.method == 'POST':
        if UserHandler().getUserIssuers(json=request.json, no_json=True):
            return UserHandler().changeRole(json=request.json)
        else:
            return jsonify(Error="User cannot change  role ID "+str(request.json)), 405
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Users/uid=<int:uid>/Delegated", methods=['GET'])
@login_required
def getDelegatedUserByID(uid):
    if request.method == 'GET':
        
        if(current_user.id == uid ):
            return UserHandler().getUsersDelegatedByID(uid=int(current_user.id))
        else:
            if int(current_user.user_role) == 4:
                return UserHandler().getUsersDelegatedByID(uid=int(uid))
            else:
                return jsonify(Error='Method not allowed for user role'), 200
    else:
        return jsonify(Error='Method not allowed.'), 405


@app.route("/Dashboard/Users/Permissions/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
# @login_required
# @mod_role_required
def geUsersAndIssuersSegmented(offset, limit):
    if request.method == 'GET':
        return UserHandler().getUsersAndIssuersSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error='Method not allowed.'), 405


@app.route("/Dashboard/Users/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
# @login_required
# @admin_role_required
def geUsersSegmented(offset, limit):
    if request.method == 'GET':
        return UserHandler().getUsersSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error='Method not allowed.'), 405


@app.route("/Dashboard/Users/roleid=<int:roleid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getAllUsersByRoleID(roleid, offset, limit):
    if request.method == 'GET':
        return UserHandler().getAllUsersByRoleIDSegmented(roleid=roleid, offset=offset, limit=limit)
    else:
        return jsonify(Error='Method not allowed.'), 405


@app.route("/Dashboard/Stats/roleid=<int:roleid>", methods=['GET'])
# @login_required
# @admin_role_required
def geNumberOdUsersByRole(roleid):
    if request.method == 'GET':
        return UserHandler().getNumberOfUsersByRole(roleid=roleid)
    else:
        return jsonify(Error='Method not allowed.'), 405
