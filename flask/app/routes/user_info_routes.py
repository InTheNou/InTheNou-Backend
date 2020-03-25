from app import app
from flask import Flask , redirect ,url_for,session,jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from app.handlers.UserHandler import UserHandler
from flask_login import login_required, logout_user,current_user
from app.oauth import admin_role_required, mod_role_required


##APP ROUTES##

@app.route("/App/Users/uid=<int:uid>", methods=['GET'])
#@login_required
#@mod_role_required
def getUserByID(uid):
    if request.method == 'GET' : return UserHandler().getUserByID(uid=uid)
    else: return jsonify(Error='Method not allowed.'), 405

    

@app.route("/App/Users/canModify/eid=<int:eid>", methods = ['GET'])
def getUsersThatCanModifyEvent(eid):
    if request.method == 'GET' : return UserHandler().getUsersThatCanModifyEvent(eid=eid)
    else: return jsonify(Error='Method not allowed.'), 405


##DASHBOARD ROUTES##
# TODO: verify the user has event creator + privileges
# TODO: Pass uid from session.
@app.route("/Dashboard/Users/changeRole", methods=['POST'])
def changeRole():
    if request.method == 'POST': return UserHandler().changeRole(json=request.json)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Users/Delegated",methods =['GET'])
#@login_required
#@admin_role_required
def getDelegatedUserByID():
    if request.method == 'GET' : return UserHandler().getUsersDelegatedByID(int(current_user.id))
    else:return jsonify(Error ='Method not allowed.'),405


@app.route("/Dashboard/Users/Permissions/offset=<int:offset>/limit=<int:limit>",methods =['GET'])
#@login_required
#@mod_role_required
def geUsersAndIssuersSegmented(offset,limit):
    if request.method == 'GET' : return UserHandler().getUsersAndIssuersSegmented(offset=offset,limit=limit)
    else:return jsonify(Error = 'Method not allowed.'),405


@app.route("/Dashboard/Users/offset=<int:offset>/limit=<int:limit>",methods =['GET'])
#@login_required
#@admin_role_required
def geUsersSegmented(offset,limit):
    if request.method == 'GET' : return UserHandler().getUsersSegmented(offset=offset,limit=limit)
    else:return jsonify(Error = 'Method not allowed.'),405

@app.route("/Dashboard/Stats/roleid=<int:roleid>",methods =['GET'])
#@login_required
#@admin_role_required
def geNumberOdUsersByRole(roleid):
    if request.method == 'GET' : return UserHandler().getNumberOfUsersByRole(roleid = roleid)
    else:return jsonify(Error = 'Method not allowed.'),405