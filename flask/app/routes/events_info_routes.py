from app import app
from flask import Flask , redirect ,url_for,session,jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from app.handlers.EventHandler import EventHandler
from app.handlers.RoomHandler import RoomHandler
from app.handlers.BuildingHandler import BuildingHandler
from app.handlers.ServiceHandler import ServiceHandler
from app.handlers.TagHandler import TagHandler


# TODO: MODIFY ROUTES TO MATCH PRE-ESTABISHED API ONCE FUNCTIONAL
# TODO: Add event-related info about related tables once DAOs/Handlers implemented.
# Automated test not set up
@app.route("/App/Events/eid=<int:eid>", methods=['GET'])
def getEventByID(eid):
    if request.method == 'GET': return EventHandler().getEventByID(eid=eid)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/eid=<int:eid>/uid=<int:uid>/Follow", methods=['POST'])
def followEvent(eid, uid):
    if request.method == 'POST': return EventHandler().setInteraction(eid=eid, uid=uid, itype="following")
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/eid=<int:eid>/uid=<int:uid>/Unfollow", methods=['POST'])
def unfollowEvent(eid, uid):
    if request.method == 'POST': return EventHandler().setInteraction(eid=eid, uid=uid, itype="unfollowed")
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/eid=<int:eid>/uid=<int:uid>/Dismiss", methods=['POST'])
def dismissEvent(eid, uid):
    if request.method == 'POST': return EventHandler().setInteraction(eid=eid, uid=uid, itype="dismissed")
    else: return jsonify(Error="Method not allowed."), 405


# TODO: Make recommendstatus pass parameters via JSON
@app.route("/App/Events/eid=<int:eid>/uid=<int:uid>/recommendstatus=<string:recommendstatus>", methods=['POST'])
def setRecommendation(eid, uid, recommendstatus):
    if request.method == 'POST': return EventHandler().setRecommendation(eid=eid, uid=uid,
                                                                         recommendstatus=recommendstatus)
    else: return jsonify(Error="Method not allowed."), 405


# Automated test not set up
@app.route("/App/Events/General/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getUpcomingGeneralEventsSegmented(uid, offset, limit):
    if request.method == 'GET': return EventHandler().getUpcomingGeneralEventsSegmented(uid=uid, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


# Automated test not set up
@app.route("/App/Events/Recommended/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getUpcomingRecommendedEventsSegmented(uid, offset, limit):
    if request.method == 'GET': return EventHandler().getUpcomingRecommendedEventsSegmented(uid=uid, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/Following/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getUpcomingFollowedEventsSegmented(uid, offset, limit):
    if request.method == 'GET': return EventHandler().getUpcomingFollowedEventsSegmented(uid=uid, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


# Automated test not set up
@app.route("/App/Events/History/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getPastFollowedEventsSegmented(uid, offset, limit):
    if request.method == 'GET': return EventHandler().getPastFollowedEventsSegmented(uid=uid, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


# Automated test not set up
@app.route("/App/Events/Created/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getEventsCreatedByUser(uid, offset, limit):
    if request.method == 'GET': return EventHandler().getEventsCreatedByUser(uid=uid, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


# Automated test not set up
# TODO: test further when event insert routes are functional.
# TODO: Consider what information should belong in JSONS.
@app.route("/App/Events/Dismissed/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getDismissedEvents(uid, offset, limit):
    if request.method == 'GET': return EventHandler().getDismissedEvents(uid=uid, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Rooms/rid=<int:rid>", methods=['GET'])
def getRoomByID(rid):
    if request.method == 'GET': return RoomHandler().getRoomByID(rid=rid)
    else: return jsonify(Error="Method not allowed."), 405


# TODO: Update Automated tests
@app.route("/App/Rooms/bid=<int:bid>/rfloor=<int:rfloor>", methods=['GET'])
def getRoomsByBuildingAndFloor(bid, rfloor):
    if request.method == 'GET': return RoomHandler().getRoomsByBuildingAndFloor(bid=bid, rfloor=rfloor)
    else: return jsonify(Error="Method not allowed."), 405


# Automated test not set up; may not be necessary, since only one room in system.
@app.route("/Dev/Buildings", methods=['GET'])
def getAllBuildings():
    if request.method == 'GET': return BuildingHandler().getAllBuildings()
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Buildings/bid=<int:bid>", methods=['GET'])
def getBuildingByID(bid):
    if request.method == 'GET': return BuildingHandler().getBuildingByID(bid=bid)
    else: return jsonify(Error="Method not allowed."), 405


# Automated test not set up
@app.route("/App/Services/sid=<int:sid>", methods=['GET'])
def getServiceByID(sid):
    if request.method == 'GET': return ServiceHandler().getServiceByID(sid=sid)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags", methods=['GET'])
def getAllTags():
    if request.method == 'GET': return TagHandler().getAllTags()
    else: return jsonify(Error="Method not allowed."), 405


# Test Route
@app.route("/App/Tags/tid=<int:tid>", methods=['GET'])
def getTagByID(tid):
    if request.method == 'GET': return TagHandler().getTagByID(tid=tid)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags/eid=<int:eid>", methods=['GET'])
def getTagsByEventID(eid):
    if request.method == 'GET': return TagHandler().getTagsByEventID(eid=eid)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags/uid=<int:uid>", methods=['GET'])
def getTagsByUserID(uid):
    if request.method == 'GET': return TagHandler().getTagsByUserID(uid=uid)
    else: return jsonify(Error="Method not allowed."), 405