from app import app
from flask import Flask , redirect ,url_for,session,jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from app.handlers.EventHandler import EventHandler
from app.handlers.RoomHandler import RoomHandler
from app.handlers.BuildingHandler import BuildingHandler
from app.handlers.ServiceHandler import ServiceHandler
from app.handlers.TagHandler import TagHandler


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


@app.route("/Dashboard/Services/website/remove", methods=['DELETE'])
def removeServiceWebsite():
    if request.method == 'DELETE': return ServiceHandler().removeServiceWebsite(request.json)
    else: return jsonify(Error="Method not allowed."), 405

@app.route("/Dashboard/Services/sid=<int:sid>/website/add",methods=['GET'])
def getServiceWebsite(sid):
    if request.method == 'GET': return ServiceHandler().insertServiceWebsite(sid=sid,json= request.json)
    else: return jsonify(Error="Method not allowed."), 405