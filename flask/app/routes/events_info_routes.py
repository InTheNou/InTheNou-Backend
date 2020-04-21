from app import app
from flask import Flask, redirect, url_for, session, jsonify, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import current_user, login_required
from app.oauth import event_creator_role_required, mod_role_required, admin_role_required, user_role_required
from app.handlers.EventHandler import EventHandler
from app.handlers.RoomHandler import RoomHandler
from app.handlers.BuildingHandler import BuildingHandler
from app.handlers.ServiceHandler import ServiceHandler
from app.handlers.TagHandler import TagHandler
from app.handlers.UserHandler import UserHandler

route_prefix = "/API"


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


@app.route(route_prefix + "/App/Events/eid=<int:eid>", methods=['GET'])
@user_role_required
def getEventByID(eid):
    if request.method == 'GET':
        return EventHandler().getEventByID(eid=eid)
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/eid=<int:eid>/uid=<int:uid>
@app.route(route_prefix + "/App/Events/eid=<int:eid>/Interaction", methods=['GET'])
@user_role_required
def getEventByIDWithInteractions(eid):
    if request.method == 'GET':
        return EventHandler().getEventByIDWithInteraction(eid=eid, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/CAT/timestamp=<string:timestamp>/uid=<int:uid>
@app.route(route_prefix + "/App/Events/CAT/timestamp=<string:timestamp>", methods=['GET'])
@user_role_required
def getEventsCreatedAfterTimestamp(timestamp):
    if request.method == 'GET':
        return EventHandler().getEventsCreatedAfterTimestamp(timestamp=timestamp, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: Update api that ecreator is no longer necessary.
@app.route(route_prefix + "/App/Events/Create", methods=['POST'])
@event_creator_role_required
def createEvent():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return EventHandler().createEvent(json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/Deleted/New/timestamp=<string:timestamp>", methods=['GET'])
@user_role_required
def getNewDeletedEvents(timestamp):
    if request.method == 'GET':
        return EventHandler().getNewDeletedEvents(timestamp=timestamp)
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/eid=<int:eid>/uid=<int:uid>/Follow
@app.route(route_prefix + "/App/Events/eid=<int:eid>/Follow", methods=['POST'])
@user_role_required
def followEvent(eid):
    if request.method == 'POST':
        return EventHandler().setInteraction(eid=eid, uid=int(current_user.id), itype="following")
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/eid=<int:eid>/uid=<int:uid>/Dismiss
@app.route(route_prefix + "/App/Events/eid=<int:eid>/Dismiss", methods=['POST'])
@user_role_required
def dismissEvent(eid):
    if request.method == 'POST':
        return EventHandler().setInteraction(eid=eid, uid=int(current_user.id), itype="dismissed")
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/eid=<int:eid>/uid=<int:uid>/Unfollow
@app.route(route_prefix + "/App/Events/eid=<int:eid>/Unfollow", methods=['POST'])
@user_role_required
def unfollowEvent(eid):
    if request.method == 'POST':
        return EventHandler().setInteraction(eid=eid, uid=int(current_user.id), itype="unfollowed")
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/eid=<int:eid>/uid=<int:uid>/estatus=<string:estatus>
@app.route(route_prefix + "/App/Events/eid=<int:eid>/estatus=<string:estatus>", methods=['POST'])
@event_creator_role_required
def setEventStatus(eid, estatus):
    if request.method == 'POST':
        # Todo: verify after merging to Dev. that this does not cause errors.
        list_of_valid_users = UserHandler().getUsersThatCanModifyEvent(eid=eid, no_json=True)
        if not list_of_valid_users or not list_of_valid_users["Users"]:
            return jsonify(Error="no users")
        else:
            for user in list_of_valid_users["Users"]:
                if user["user_id"][0] == int(current_user.id):
                    return EventHandler().setEventStatus(eid=eid, uid=int(current_user.id), estatus=estatus)
            return jsonify(Error="User is not authorized to modify this event."), 403
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/eid=<int:eid>/uid=<int:uid>/recommendstatus=<string:recommendstatus>
@app.route(route_prefix + "/App/Events/eid=<int:eid>/recommendstatus=<string:recommendstatus>", methods=['POST'])
@user_role_required
def setRecommendation(eid, recommendstatus):
    if request.method == 'POST':
        return EventHandler().setRecommendation(eid=eid, uid=int(current_user.id), recommendstatus=recommendstatus)
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/Created/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>
@app.route(route_prefix + "/App/Events/Created/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getEventsCreatedByUser(offset, limit):
    if request.method == 'GET':
        return EventHandler().getEventsCreatedByUser(uid=int(current_user.id), offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/Dismissed/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>
@app.route(route_prefix + "/App/Events/Dismissed/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getDismissedEvents(offset, limit):
    if request.method == 'GET':
        return EventHandler().getDismissedEvents(uid=int(current_user.id), offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/Following/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>
@app.route(route_prefix + "/App/Events/Following/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getUpcomingFollowedEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingFollowedEventsSegmented(uid=int(current_user.id), offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/General/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>
@app.route(route_prefix + "/App/Events/General/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getUpcomingGeneralEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingGeneralEventsSegmented(uid=int(current_user.id), offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/General/search=<string:searchstring>/offset=<int:offset>/limit=<int:limit>/uid=<int:uid>
@app.route(route_prefix + "/App/Events/General/search=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getUpcomingGeneralEventsByKeywordsSegmented(searchstring, offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingGeneralEventsByKeywordsSegmented(uid=int(current_user.id),
                                                                          searchstring=searchstring,
                                                                          offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/History/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>
@app.route(route_prefix + "/App/Events/History/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getPastFollowedEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getPastFollowedEventsSegmented(uid=int(current_user.id), offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/Recommended/uid=<int:uid>/offset=<int:offset>/limit=<int:limit>
@app.route(route_prefix + "/App/Events/Recommended/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getUpcomingRecommendedEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingRecommendedEventsSegmented(uid=int(current_user.id),
                                                                    offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# old route: /App/Events/Recommended/search=<string:searchstring>/offset=<int:offset>/limit=<int:limit>/uid=<int:uid>
@app.route(route_prefix + "/App/Events/Recommended/search=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getUpcomingRecommendedEventsByKeywordSegmented(searchstring, offset, limit):
    if request.method == 'GET':
        return EventHandler().getUpcomingRecommendedEventsByKeywordSegmented(uid=int(current_user.id),
                                                                             searchstring=searchstring,
                                                                             offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/Dashboard/Events/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@mod_role_required
def getAllEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getAllEventsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/Dashboard/Events/ecreator=<int:ecreator>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@mod_role_required
def getEventsCreatedByOtherUser(ecreator, offset, limit):
    if request.method == 'GET':
        # Json used because current implementation of getUserIssuers() requires it.
        issuer_check_json = jsonify({"id": int(current_user.id), "uid": ecreator, "roleid": 1})
        is_user_issuer = UserHandler().getUserIssuers(json=issuer_check_json, no_json=True)
        if is_user_issuer:
            return EventHandler().getEventsCreatedByUser(uid=ecreator, offset=offset, limit=limit)
        return jsonify(Error="Currently logged in user is not authorized to "
                             "view events created by the requested user."), 403
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/Dashboard/Events/Deleted/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@mod_role_required
def getAllDeletedEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getAllDeletedEventsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/Dashboard/Events/Past/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@mod_role_required
def getAllPastEventsSegmented(offset, limit):
    if request.method == 'GET':
        return EventHandler().getAllPastEventsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Rooms/rid=<int:rid>", methods=['GET'])
@user_role_required
def getRoomByID(rid):
    if request.method == 'GET':
        return RoomHandler().getRoomByID(rid=rid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Rooms/babbrev=<string:babbrev>/rcode=<string:rcode>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getRoomsByCodeSearchSegmented(babbrev, rcode, offset, limit):
    if request.method == 'GET':
        return RoomHandler().getRoomsByCodeSearchSegmented(babbrev=babbrev, rcode=rcode, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Rooms/searchstring=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getRoomsByKeywordSegmented(searchstring, offset, limit):
    if request.method == 'GET':
        return RoomHandler().getRoomsByKeywordSegmented(searchstring=searchstring, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Rooms/bid=<int:bid>/rfloor=<int:rfloor>", methods=['GET'])
@user_role_required
def getRoomsByBuildingAndFloor(bid, rfloor):
    if request.method == 'GET':
        return RoomHandler().getRoomsByBuildingAndFloor(bid=bid, rfloor=rfloor)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Buildings/bid=<int:bid>", methods=['GET'])
@user_role_required
def getBuildingByID(bid):
    if request.method == 'GET':
        return BuildingHandler().getBuildingByID(bid=bid)
    else:
        return jsonify(Error="Method not allowed."), 405


# Automated test not set up; may not be necessary, since only one room in system.
@app.route(route_prefix + "/Dev/Buildings", methods=['GET'])
@user_role_required
def getAllBuildings():
    if request.method == 'GET':
        return BuildingHandler().getAllBuildings()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Buildings/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getAllBuildingsSegmented(offset, limit):
    if request.method == 'GET':
        return BuildingHandler().getAllBuildingsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# Automated test not set up
@app.route(route_prefix + "/App/Buildings/Search/searchstring=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getBuildingsByKeywords(searchstring, offset, limit):
    if request.method == 'GET':
        return BuildingHandler().getBuildingsByKeyword(keyword=searchstring,
                                                       offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Services/searchstring=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getServicesByKeywords(searchstring, offset, limit):
    if request.method == 'GET':
        return ServiceHandler().getServicesByKeywords(searchstring=searchstring, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# This route is used before signup is called/before session is created.
# TODO: Figure out if there is some other way to secure this route without sessions.
@app.route(route_prefix + "/App/Tags", methods=['GET'])
def getAllTags():
    if request.method == 'GET':
        return TagHandler().getAllTags()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Tags/eid=<int:eid>", methods=['GET'])
@user_role_required
def getTagsByEventID(eid):
    if request.method == 'GET':
        return TagHandler().getTagsByEventID(eid=eid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Tags/tid=<int:tid>", methods=['GET'])
@user_role_required
def getTagByID(tid):
    if request.method == 'GET':
        return TagHandler().getTagByID(tid=tid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Tags/UserTags", methods=['GET'])
@user_role_required
def getTagsByUserIDSession():
    if request.method == 'GET':
        return TagHandler().getTagsByUserID(uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Tags/User/Remove", methods=['POST'])
@user_role_required
def setUserTagsToZero():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return TagHandler().batchSetUserTags(uid=int(current_user.id),
                                             json=request.json, weight=0)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Tags/User/Add", methods=['POST'])
@user_role_required
def setUserTagsToDefault():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return TagHandler().batchSetUserTags(uid=int(current_user.id),
                                             json=request.json, weight=100)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/Dashboard/Tags/Create", methods=['POST'])
@admin_role_required
def createTag():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return TagHandler().createTags(jsonTags=request.json)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/Dashboard/Tags/tid=<int:tid>/Edit", methods=['POST'])
@admin_role_required
def editTagName(tid):
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return TagHandler().editTagName(tid=tid, json=request.json)

    else:
        return jsonify(Error="Method not allowed."), 405
