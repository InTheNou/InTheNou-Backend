from app import app
from flask import Flask , redirect ,url_for,session,jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from app.handlers.EventHandler import EventHandler
from app.handlers.RoomHandler import RoomHandler
from app.handlers.BuildingHandler import BuildingHandler
from app.handlers.ServiceHandler import ServiceHandler
from app.handlers.TagHandler import TagHandler
from app.handlers.PhoneHandler import PhoneHandler
from app.handlers.WebsiteHandler import WebsiteHandler
# Automated test not set up
@app.route("/App/Services/sid=<int:sid>", methods=['GET'])
def getServiceByID(sid):
    if request.method == 'GET': return ServiceHandler().getServiceByID(sid=sid)
    else: return jsonify(Error="Method not allowed."), 405


###DASHBOARD ROUTES####

@app.route("/Dashboard/Services/create", methods=['POST'])
def createService():
    if request.method == 'POST': return ServiceHandler().createService(json=request.json)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Services/sid=<int:sid>/website/remove", methods=['POST'])
def removeServiceWebsite(sid):
    if request.method == 'POST': return WebsiteHandler().removeServiceWebsite(sid=sid,json=request.json)
    else: return jsonify(Error="Method not allowed."), 405

@app.route("/Dashboard/Services/sid=<int:sid>/website/add",methods=['GET'])
def addServiceWebsite(sid):
    if request.method == 'GET': return WebsiteHandler().insertServiceWebsite(sid=sid,json= request.json)
    else: return jsonify(Error="Method not allowed."), 405

@app.route("/Dashboard/Services/sid=<int:sid>/phone/add",methods=['GET'])
def addServicePhone(sid):
    if request.method == 'GET': return PhoneHandler().insertServicePhone(sid=sid,json= request.json)
    else: return jsonify(Error="Method not allowed."), 405
    
@app.route("/Dashboard/Services/sid=<int:sid>/phone/remove", methods=['POST'])
def removeServicePhone(sid):
    if request.method == 'POST': return PhoneHandler().removePhoneByServiceID(sid=sid,json=request.json)
    else: return jsonify(Error="Method not allowed."), 405