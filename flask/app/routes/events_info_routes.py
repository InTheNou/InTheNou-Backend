from app import app
from flask import Flask , redirect ,url_for,session,jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from app.handlers.EventHandler import EventHandler
from app.handlers.RoomHandler import RoomHandler
from app.handlers.BuildingHandler import BuildingHandler
from app.handlers.ServiceHandler import ServiceHandler
from app.handlers.TagHandler import TagHandler


@app.errorhandler(400)
def bad_request_error(error):
    return jsonify(Error=str(error)), 400


@app.errorhandler(404)
def not_found_error(error):
    return jsonify(Error="Invalid URI parameters: " + str(request.url)), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify(Error="Internal Server Error while accessing route: " +
                         str(request.url) + " : " + str(error)), 500


# TODO: Add Event Creator information to event routes during integration.
# TODO: Change parameter passing from URI to URI + JSON + Session during integration.
# NOTE: all personal uid's will be sent via sessions, or json during integration.
@app.route("/App/Events/eid=<int:eid>", methods=['GET'])
def getEventByID(eid):
    if request.method == 'GET': return EventHandler().getEventByID(eid=eid)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/Deleted/New", methods=['GET'])
def getNewDeletedEvents():
    if request.method == 'GET':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return EventHandler().getNewDeletedEvents(json=request.json)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/CAT", methods=['GET'])
def getEventsCreatedAfterTimestamp():
    if request.method == 'GET':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return EventHandler().getEventsCreatedAfterTimestamp(json=request.json)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Events/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getAllEventsSegmented(offset, limit):
    if request.method == 'GET': return EventHandler().getAllEventsSegmented(offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Events/Past/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getAllPastEventsSegmented(offset, limit):
    if request.method == 'GET': return EventHandler().getAllPastEventsSegmented(offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Events/Deleted/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getAllDeletedEventsSegmented(offset, limit):
    if request.method == 'GET': return EventHandler().getAllDeletedEventsSegmented(offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


# TODO: verify the user has event creator + privileges
# TODO: Pass uid from session.
@app.route("/App/Events/Create", methods=['POST'])
def createEvent():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return EventHandler().createEvent(json=request.json)
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
    if request.method == 'POST':
        return EventHandler().setRecommendation(eid=eid, uid=uid, recommendstatus=recommendstatus)
    else: return jsonify(Error="Method not allowed."), 405


# TODO: use UID to verify user's permission to delete an event.
# TODO: Make estatus pass parameters via JSON
@app.route("/App/Events/eid=<int:eid>/uid=<int:uid>/estatus=<string:estatus>", methods=['POST'])
def setEventStatus(eid, uid, estatus):
    if request.method == 'POST': return EventHandler().setEventStatus(eid=eid, uid=uid, estatus=estatus)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/General/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getUpcomingGeneralEventsSegmented(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingGeneralEventsSegmented(uid=uid, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/General/Keyword/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getUpcomingGeneralEventsByKeywordsSegmented(offset, limit):                            # Make this with session!
    if request.method == 'GET':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return EventHandler().getUpcomingGeneralEventsByKeywordsSegmented(uid=request.json['uid'], json=request.json,
                                                                          offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/Recommended/Keyword/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getUpcomingRecommendedEventsByKeywordSegmented(offset, limit):                           # Make this with session!
    if request.method == 'GET':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return EventHandler().getUpcomingRecommendedEventsByKeywordSegmented(uid=request.json['uid'], json=request.json,
                                                                             offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/Recommended/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getUpcomingRecommendedEventsSegmented(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingRecommendedEventsSegmented(uid=uid, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/Following/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getUpcomingFollowedEventsSegmented(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingFollowedEventsSegmented(uid=uid, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/History/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getPastFollowedEventsSegmented(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getPastFollowedEventsSegmented(uid=uid, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


# Use session instead of uri for uid.
@app.route("/App/Events/Created/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getEventsCreatedByUser(uid, offset, limit):
    if request.method == 'GET': return EventHandler().getEventsCreatedByUser(uid=uid, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


# Use session to authorize, but get UID to check from json
@app.route("/Dashboard/Events/Created/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getEventsCreatedByOtherUser(offset, limit):
    if request.method == 'GET':
        # TODO: VERIFY IF SESSION USER IS AUTHORIZED FOR THE USER THEY ARE SEARCHING.
        if 'uid' in request.json:
            return EventHandler().getEventsCreatedByUser(uid=request.json['uid'], offset=offset, limit=limit)
        else: return jsonify(Error="Missing key: uid."), 401
    else: return jsonify(Error="Method not allowed."), 405


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


@app.route("/App/Rooms/Search/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getRoomsBySearch(offset, limit):
    if request.method == 'GET':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return RoomHandler().getRoomsBySearch(json=request.json, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


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


@app.route("/App/Services/Search/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getServicesByKeywords(offset, limit):
    if request.method == 'GET':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return ServiceHandler().getServicesByKeywords(json=request.json, offset=offset, limit=limit)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags", methods=['GET'])
def getAllTags():
    if request.method == 'GET': return TagHandler().getAllTags()
    else: return jsonify(Error="Method not allowed."), 405


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


@app.route("/App/Tags/User/Remove", methods=['POST'])
def setUserTagsToZero():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return TagHandler().batchSetUserTags(json=request.json, weight=0, uid=None)
    else: return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags/User/Add", methods=['POST'])
def setUserTagsToDefault():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return TagHandler().batchSetUserTags(json=request.json, weight=100, uid=None)
    else: return jsonify(Error="Method not allowed."), 405
