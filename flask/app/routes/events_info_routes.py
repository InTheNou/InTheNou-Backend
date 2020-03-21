from app import app
from flask import Flask , redirect ,url_for,session,jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from app.handlers.EventHandler import EventHandler
from app.handlers.RoomHandler import RoomHandler
from app.handlers.BuildingHandler import BuildingHandler


# TODO: MODIFY ROUTES TO MATCH PRE-ESTABISHED API ONCE FUNCTIONAL
# TODO: Add event-related info about related tables once DAOs/Handlers implemented.
@app.route("/App/Events/eid=<int:eid>", methods=['GET'])
def getEventByID(eid):
    if request.method == 'GET': return EventHandler().getEventByID(eid=eid)
    else: return jsonify(Error="Method not allowed."), 405


# TODO: Add event-related info about related tables once DAOs/Handlers implemented.
@app.route("/App/Rooms/rid=<int:rid>", methods=['GET'])
def getRoomByID(rid):
    if request.method == 'GET': return RoomHandler().getRoomByID(rid=rid)
    else: return jsonify(Error="Method not allowed."), 405


# TODO: Add event-related info about related tables once DAOs/Handlers implemented.
@app.route("/App/Buildings/bid=<int:bid>", methods=['GET'])
def getBuildingByID(bid):
    if request.method == 'GET': return BuildingHandler().getBuildingByID(bid=bid)
    else: return jsonify(Error="Method not allowed."), 405

