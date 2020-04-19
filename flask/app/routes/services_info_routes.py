from app import app
from flask import Flask, redirect, url_for, session, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from app.handlers.EventHandler import EventHandler
from app.handlers.RoomHandler import RoomHandler
from app.handlers.BuildingHandler import BuildingHandler
from app.handlers.ServiceHandler import ServiceHandler
from app.handlers.TagHandler import TagHandler
from app.handlers.PhoneHandler import PhoneHandler
from app.handlers.WebsiteHandler import WebsiteHandler
# Automated test not set up
@app.route("/API/App/Services/sid=<int:sid>", methods=['GET'])
def getServiceByID(sid):
    if request.method == 'GET':
        return ServiceHandler().getServiceByID(sid=sid)
    else:
        return jsonify(Error="Method not allowed."), 405


###DASHBOARD ROUTES####
@app.route("/API/Dashboard/Services/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getServicesSegmented(limit, offset):
    if request.method == 'GET':
        return ServiceHandler().getServicesSegmented(limit=limit, offset=offset)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/API/Dashboard/Rooms/rid=<int:rid>/Services", methods=['GET'])
def getServicesByRoomID(rid):
    if request.method == 'GET':
        return ServiceHandler().getServicesByRoomID(rid)
    else:
        return jsonify(Error="Method not allowed."), 405

# TODO: verify this is working with audit
@app.route("/API/Dashboard/Services/create", methods=['POST'])
def createService():
    if request.method == 'POST':
        return ServiceHandler().createService(json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/API/Dashboard/Services/sid=<int:sid>/website/remove", methods=['POST'])
def removeServiceWebsite(sid):
    if request.method == 'POST':
        return WebsiteHandler().removeServiceWebsite(sid=sid, json=request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/API/Dashboard/Services/sid=<int:sid>/website/add", methods=['POST'])
def addServiceWebsite(sid):
    if request.method == 'POST':
        return WebsiteHandler().insertServiceWebsite(sid=sid, json=request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: ENSURE THE AUDIT CHANGE WORKS FOR THIS ROUTE.
@app.route("/API/Dashboard/Services/sid=<int:sid>/phone/add", methods=['POST'])
def addServicePhone(sid):
    if request.method == 'POST':
        return PhoneHandler().insertServicePhone(sid=sid, uid=int(current_user.id), json=request.json)
    else:
        return jsonify(Error="Method not allowed."), 405

# TODO: ENSURE THE AUDIT CHANGE WORKS FOR THIS ROUTE.
@app.route("/API/Dashboard/Services/sid=<int:sid>/phone/remove", methods=['POST'])
def removeServicePhone(sid):
    if request.method == 'POST':
        return PhoneHandler().removePhoneByServiceID(sid=sid, json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: check that this route is using audit properly
@app.route("/API/Dashboard/Services/sid=<int:sid>/update", methods=['POST'])
def updateService(sid):
    if request.method == 'POST':
        return ServiceHandler().updateServiceInformation(sid=sid, json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: check that this route is using audit properly
@app.route("/API/Dashboard/Services/sid=<int:sid>/delete", methods=['POST'])
def deleteService(sid):
    if request.method == 'POST':
        return ServiceHandler().deleteService(sid=sid, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: check that this route is using audit properly
@app.route("/API/Dashboard/Rooms/rid=<int:rid>/changeCoordinates", methods=['POST'])
def changeRoomCoordinates(rid):
    if request.method == 'POST':
        return RoomHandler().changeRoomCoordinates(rid=rid, json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405
