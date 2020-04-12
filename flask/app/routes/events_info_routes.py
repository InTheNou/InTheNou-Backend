from app import app
from flask import Flask, redirect, url_for, session, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import current_user, login_required
from app.oauth import event_creator_role_required, mod_role_required, admin_role_required
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


@app.route("/App/Events/eid=<int:eid>", methods=['GET'])
@login_required
def getEventByID(eid):
    if request.method == 'GET':
        return EventHandler().getEventByID(eid=eid)
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/eid=<int:eid>/uid=<int:uid>
@app.route("/App/Events/eid=<int:eid>/Interaction", methods=['GET'])
@login_required
def getEventByIDWithInteractions(eid):
    if request.method == 'GET':
        return EventHandler().getEventByIDWithInteraction(eid=eid, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/CAT/timestamp=<string:timestamp>/uid=<int:uid>
@app.route("/App/Events/CAT/timestamp=<string:timestamp>", methods=['GET'])
@login_required
def getEventsCreatedAfterTimestamp(timestamp):
    if request.method == 'GET':
        return EventHandler().getEventsCreatedAfterTimestamp(timestamp=timestamp, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: Update api that ecreator is no longer necessary.
@app.route("/App/Events/Create", methods=['POST'])
@login_required
@event_creator_role_required
def createEvent():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return EventHandler().createEvent(json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Events/Deleted/New/timestamp=<string:timestamp>", methods=['GET'])
@login_required
def getNewDeletedEvents(timestamp):
    if request.method == 'GET':
        return EventHandler().getNewDeletedEvents(timestamp=timestamp)
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/eid=<int:eid>/uid=<int:uid>/Follow
@app.route("/App/Events/eid=<int:eid>/Follow", methods=['POST'])
@login_required
def followEvent(eid):
    if request.method == 'POST':
        return EventHandler().setInteraction(eid=eid, uid=int(current_user.id), itype="following")
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/eid=<int:eid>/uid=<int:uid>/Dismiss
@app.route("/App/Events/eid=<int:eid>/Dismiss", methods=['POST'])
@login_required
def dismissEvent(eid):
    if request.method == 'POST':
        return EventHandler().setInteraction(eid=eid, uid=int(current_user.id), itype="dismissed")
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/eid=<int:eid>/uid=<int:uid>/Unfollow
@app.route("/App/Events/eid=<int:eid>/Unfollow", methods=['POST'])
@login_required
def unfollowEvent(eid):
    if request.method == 'POST':
        return EventHandler().setInteraction(eid=eid, uid=int(current_user.id), itype="unfollowed")
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: use UID to verify user's permission to delete an event.
# old route: /App/Events/eid=<int:eid>/uid=<int:uid>/estatus=<string:estatus>
@app.route("/App/Events/eid=<int:eid>/estatus=<string:estatus>", methods=['POST'])
@login_required
def setEventStatus(eid, estatus):
    if request.method == 'POST':
        return EventHandler().setEventStatus(eid=eid, uid=int(current_user.id), estatus=estatus)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: PASS UID BY SESSION
@app.route("/App/Events/eid=<int:eid>/uid=<int:uid>/recommendstatus=<string:recommendstatus>", methods=['POST'])
@login_required
def setRecommendation(eid, uid, recommendstatus):
    if request.method == 'POST':
        return EventHandler().setRecommendation(eid=eid, uid=uid, recommendstatus=recommendstatus)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: PASS UID BY SESSION
@app.route("/App/Events/Created/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getEventsCreatedByUser(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getEventsCreatedByUser(uid=uid, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: PASS UID BY SESSION
@app.route("/App/Events/Dismissed/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getDismissedEvents(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getDismissedEvents(uid=uid, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405

# TODO: PASS UID BY SESSION
@app.route("/App/Events/Following/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getUpcomingFollowedEventsSegmented(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingFollowedEventsSegmented(uid=uid, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: PASS UID BY SESSION
@app.route("/App/Events/General/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getUpcomingGeneralEventsSegmented(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingGeneralEventsSegmented(uid=uid, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405

# TODO: PASS UID BY SESSION
@app.route("/App/Events/General/search=<string:searchstring>/offset=<int:offset>/limit=<int:limit>/uid=<int:uid>", methods=['GET'])
@login_required
def getUpcomingGeneralEventsByKeywordsSegmented(searchstring, offset, limit, uid):
    if request.method == 'GET':
        return EventHandler().getUpcomingGeneralEventsByKeywordsSegmented(uid=uid, searchstring=searchstring,
                                                                          offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: PASS UID BY SESSION
@app.route("/App/Events/History/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getPastFollowedEventsSegmented(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getPastFollowedEventsSegmented(uid=uid, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: PASS UID BY SESSION
@app.route("/App/Events/Recommended/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getUpcomingRecommendedEventsSegmented(uid, offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingRecommendedEventsSegmented(uid=uid, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: PASS UID BY SESSION
@app.route("/App/Events/Recommended/search=<string:searchstring>/offset=<int:offset>/limit=<int:limit>/uid=<int:uid>", methods=['GET'])
@login_required
def getUpcomingRecommendedEventsByKeywordSegmented(searchstring, offset, limit, uid):
    if request.method == 'GET':
        return EventHandler().getUpcomingRecommendedEventsByKeywordSegmented(uid=uid, searchstring=searchstring,
                                                                             offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO NOT SURE IF THIS SHOULD VERIFY PRIVILEGES
@app.route("/Dashboard/Events/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getAllEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getAllEventsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# Use session to authorize, but get UID to check from json
@app.route("/Dashboard/Events/ecreator=<int:ecreator>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getEventsCreatedByOtherUser(ecreator, offset, limit):
    if request.method == 'GET':
        # TODO: VERIFY IF SESSION USER IS AUTHORIZED FOR THE USER THEY ARE SEARCHING.
        return EventHandler().getEventsCreatedByUser(uid=ecreator, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO NOT SURE IF THIS SHOULD VERIFY PRIVILEGES
@app.route("/Dashboard/Events/Deleted/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getAllDeletedEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getAllDeletedEventsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO NOT SURE IF THIS SHOULD VERIFY PRIVILEGES
@app.route("/Dashboard/Events/Past/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getAllPastEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getAllPastEventsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Rooms/rid=<int:rid>", methods=['GET'])
@login_required
def getRoomByID(rid):
    if request.method == 'GET':
        return RoomHandler().getRoomByID(rid=rid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Rooms/babbrev=<string:babbrev>/rcode=<string:rcode>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getRoomsByCodeSearchSegmented(babbrev, rcode, offset, limit):
    if request.method == 'GET':
        return RoomHandler().getRoomsByCodeSearchSegmented(babbrev=babbrev, rcode=rcode, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Rooms/searchstring=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getRoomsByKeywordSegmented(searchstring, offset, limit):
    if request.method == 'GET':
        return RoomHandler().getRoomsByKeywordSegmented(searchstring=searchstring, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Rooms/bid=<int:bid>/rfloor=<int:rfloor>", methods=['GET'])
@login_required
def getRoomsByBuildingAndFloor(bid, rfloor):
    if request.method == 'GET':
        return RoomHandler().getRoomsByBuildingAndFloor(bid=bid, rfloor=rfloor)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Buildings/bid=<int:bid>", methods=['GET'])
@login_required
def getBuildingByID(bid):
    if request.method == 'GET':
        return BuildingHandler().getBuildingByID(bid=bid)
    else:
        return jsonify(Error="Method not allowed."), 405


# Automated test not set up; may not be necessary, since only one room in system.
@app.route("/Dev/Buildings", methods=['GET'])
@login_required
def getAllBuildings():
    if request.method == 'GET':
        return BuildingHandler().getAllBuildings()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Buildings/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getAllBuildingsSegmented(offset, limit):
    if request.method == 'GET':
        return BuildingHandler().getAllBuildingsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405

# Automated test not set up
@app.route("/App/Buildings/Search/searchstring=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getBuildingsByKeywords(searchstring, offset, limit):
    if request.method == 'GET':
        return BuildingHandler().getBuildingsByKeyword(keyword=searchstring,
                                                       offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Services/searchstring=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@login_required
def getServicesByKeywords(searchstring, offset, limit):
    if request.method == 'GET':
        return ServiceHandler().getServicesByKeywords(searchstring=searchstring, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags", methods=['GET'])
@login_required
def getAllTags():
    if request.method == 'GET':
        return TagHandler().getAllTags()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags/eid=<int:eid>", methods=['GET'])
@login_required
def getTagsByEventID(eid):
    if request.method == 'GET':
        return TagHandler().getTagsByEventID(eid=eid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/App/Tags/tid=<int:tid>", methods=['GET'])
@login_required
def getTagByID(tid):
    if request.method == 'GET':
        return TagHandler().getTagByID(tid=tid)
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


# TODO: PASS UID INSTEAD OF JSON
@app.route("/App/Tags/User/Remove", methods=['POST'])
@login_required
def setUserTagsToZero():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return TagHandler().batchSetUserTags(json=request.json, weight=0, uid=None)
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: PASS UID INSTEAD OF JSON
@app.route("/App/Tags/User/Add", methods=['POST'])
@login_required
def setUserTagsToDefault():
    if request.method == 'POST':
        return TagHandler().batchSetUserTags(json=request.json, weight=100)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Tags/Create", methods=['POST'])
@login_required
@admin_role_required
def createTag():
    if request.method == 'POST':
        return TagHandler().createTags(jsonTags=request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/Dashboard/Tags/tid=<int:tid>/Edit", methods=['POST'])
@login_required
@mod_role_required
def editTagName(tid):
    if request.method == 'POST':
        return TagHandler().editTagName(tid=tid, json=request.json)

    else:
        return jsonify(Error="Method not allowed."), 405
