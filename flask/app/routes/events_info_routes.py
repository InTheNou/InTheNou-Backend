from app import app
from flask import Flask, redirect, url_for, session, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import current_user, login_required
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


# TODO: Change parameter passing from URI to URI + JSON + Session during integration.
# NOTE: all personal uid's will be sent via sessions, or json during integration.
@app.route("/App/Events/eid=<int:eid>", methods=['GET'])
def getEventByID(eid):
    if request.method == 'GET':
        return EventHandler().getEventByID(eid=eid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/eid=<int:eid>/uid=<int:uid>", methods=['GET'])
def getEventByIDWithInteractions(eid, uid):
    if request.method == 'GET':
        return EventHandler().getEventByIDWithInteraction(eid=eid, uid=uid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/CAT/timestamp=<string:timestamp>/uid=<int:uid>", methods=['GET'])
def getEventsCreatedAfterTimestamp(timestamp, uid):
    if request.method == 'GET':
        return EventHandler().getEventsCreatedAfterTimestamp(timestamp=timestamp, uid=uid)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: verify the user has event creator + privileges
# TODO: Pass uid from session.
@app.route("/App/Events/Create", methods=['POST'])
def createEvent():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return EventHandler().createEvent(json=request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/Deleted/New/timestamp=<string:timestamp>", methods=['GET'])
def getNewDeletedEvents(timestamp):
    if request.method == 'GET':
        return EventHandler().getNewDeletedEvents(timestamp=timestamp)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/eid=<int:eid>/uid=<int:uid>/Follow", methods=['POST'])
def followEvent(eid, uid):
    if request.method == 'POST':
        return EventHandler().setInteraction(eid=eid, uid=uid, itype="following")
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/eid=<int:eid>/uid=<int:uid>/Dismiss", methods=['POST'])
def dismissEvent(eid, uid):
    if request.method == 'POST':
        return EventHandler().setInteraction(eid=eid, uid=uid, itype="dismissed")
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/eid=<int:eid>/uid=<int:uid>/Unfollow", methods=['POST'])
def unfollowEvent(eid, uid):
    if request.method == 'POST':
        return EventHandler().setInteraction(eid=eid, uid=uid, itype="unfollowed")
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: use UID to verify user's permission to delete an event.
@app.route("/App/Events/eid=<int:eid>/uid=<int:uid>/estatus=<string:estatus>", methods=['POST'])
def setEventStatus(eid, uid, estatus):
    if request.method == 'POST':
        return EventHandler().setEventStatus(eid=eid, uid=uid, estatus=estatus)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/eid=<int:eid>/uid=<int:uid>/recommendstatus=<string:recommendstatus>", methods=['POST'])
def setRecommendation(eid, uid, recommendstatus):
    if request.method == 'POST':
        return EventHandler().setRecommendation(eid=eid, uid=uid, recommendstatus=recommendstatus)
    else:
        return jsonify(Error="Method not allowed."), 405


# Use session instead of uri for uid.
@app.route("/App/Events/Created/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getEventsCreatedByUser(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getEventsCreatedByUser(uid=uid, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/Dismissed/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getDismissedEvents(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getDismissedEvents(uid=uid, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/Following/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getUpcomingFollowedEventsSegmented(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingFollowedEventsSegmented(uid=uid, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/General/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getUpcomingGeneralEventsSegmented(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingGeneralEventsSegmented(uid=uid, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/General/search=<string:searchstring>/offset=<int:offset>/limit=<int:limit>/uid=<int:uid>", methods=['GET'])
# Make this with session!
def getUpcomingGeneralEventsByKeywordsSegmented(searchstring, offset, limit, uid):
    if request.method == 'GET':
        return EventHandler().getUpcomingGeneralEventsByKeywordsSegmented(uid=uid, searchstring=searchstring,
                                                                          offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/History/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getPastFollowedEventsSegmented(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getPastFollowedEventsSegmented(uid=uid, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/Recommended/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getUpcomingRecommendedEventsSegmented(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingRecommendedEventsSegmented(uid=uid, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/Recommended/search=<string:searchstring>/offset=<int:offset>/limit=<int:limit>/uid=<int:uid>", methods=['GET'])
# Make this with session!
def getUpcomingRecommendedEventsByKeywordSegmented(searchstring, offset, limit, uid):
    if request.method == 'GET':
        return EventHandler().getUpcomingRecommendedEventsByKeywordSegmented(uid=uid, searchstring=searchstring,
                                                                             offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Events/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getAllEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getAllEventsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# Use session to authorize, but get UID to check from json
@app.route("/Dashboard/Events/ecreator=<int:ecreator>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getEventsCreatedByOtherUser(ecreator, offset, limit):
    if request.method == 'GET':
        # TODO: VERIFY IF SESSION USER IS AUTHORIZED FOR THE USER THEY ARE SEARCHING.
        return EventHandler().getEventsCreatedByUser(uid=ecreator, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Events/Deleted/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getAllDeletedEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getAllDeletedEventsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Events/Past/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getAllPastEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getAllPastEventsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Rooms/rid=<int:rid>", methods=['GET'])
def getRoomByID(rid):
    if request.method == 'GET':
        return RoomHandler().getRoomByID(rid=rid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Rooms/babbrev=<string:babbrev>/rcode=<string:rcode>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getRoomsByCodeSearchSegmented(babbrev, rcode, offset, limit):
    if request.method == 'GET':
        return RoomHandler().getRoomsByCodeSearchSegmented(babbrev=babbrev, rcode=rcode, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Rooms/searchstring=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getRoomsByKeywordSegmented(searchstring, offset, limit):
    if request.method == 'GET':
        return RoomHandler().getRoomsByKeywordSegmented(searchstring=searchstring, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Rooms/bid=<int:bid>/rfloor=<int:rfloor>", methods=['GET'])
def getRoomsByBuildingAndFloor(bid, rfloor):
    if request.method == 'GET':
        return RoomHandler().getRoomsByBuildingAndFloor(bid=bid, rfloor=rfloor)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Buildings/bid=<int:bid>", methods=['GET'])
def getBuildingByID(bid):
    if request.method == 'GET':
        return BuildingHandler().getBuildingByID(bid=bid)
    else:
        return jsonify(Error="Method not allowed."), 405


# Automated test not set up; may not be necessary, since only one room in system.
@app.route("/Dev/Buildings", methods=['GET'])
def getAllBuildings():
    if request.method == 'GET':
        return BuildingHandler().getAllBuildings()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Buildings/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getAllBuildingsSegmented(offset, limit):
    if request.method == 'GET':
        return BuildingHandler().getAllBuildingsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# Automated test not set up
@app.route("/App/Buildings/Search/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getBuildingsByKeywords(offset, limit):
    if request.method == 'GET':
        return BuildingHandler().getBuildingsByKeyword(json=request.json,
                                                       offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Services/Search/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
def getServicesByKeywords(offset, limit):
    if request.method == 'GET':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return ServiceHandler().getServicesByKeywords(json=request.json, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags", methods=['GET'])
def getAllTags():
    if request.method == 'GET':
        return TagHandler().getAllTags()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags/eid=<int:eid>", methods=['GET'])
def getTagsByEventID(eid):
    if request.method == 'GET':
        return TagHandler().getTagsByEventID(eid=eid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags/tid=<int:tid>", methods=['GET'])
def getTagByID(tid):
    if request.method == 'GET':
        return TagHandler().getTagByID(tid=tid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags/uid=<int:uid>", methods=['GET'])
def getTagsByUserID(uid):
    if request.method == 'GET':
        return TagHandler().getTagsByUserID(uid=uid)
    else:
        return jsonify(Error="Method not allowed."), 405


# Test route for session testing
# No automated test setup yet.
@app.route("/App/Tags/UserTags", methods=['GET'])
@login_required
def getTagsByUserIDSession():
    if request.method == 'GET':
        return TagHandler().getTagsByUserID(uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags/User/Remove", methods=['POST'])
def setUserTagsToZero():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return TagHandler().batchSetUserTags(json=request.json, weight=0, uid=None)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags/User/Add", methods=['POST'])
def setUserTagsToDefault():
    if request.method == 'POST':
        return TagHandler().batchSetUserTags(json=request.json, weight=100)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Tags/Create", methods=['POST'])
def createTag():
    if request.method == 'POST':
        return TagHandler().createTags(jsonTags=request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Tags/tid=<int:tid>/Edit", methods=['POST'])
def editTagName(tid):
    if request.method == 'POST':
        return TagHandler().editTagName(tid=tid, json=request.json)

    else:
        return jsonify(Error="Method not allowed."), 405
