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
    """
       .. py:decorator:: user_role_required

       Uses :func:`~app.handlers.EventHandler.EventHandler.getEventByID`

       Get Event By ID

       .. :quickref: Event; Get Event By bid

       :param eid: Event ID
       :type eid: int
       :return: JSON

       **Example request**:

       .. sourcecode:: http

         GET /API/App/Events/eid=1 HTTP/1.1
         Host: inthenou.uprm.edu
         Accept: application/json

       **Example response**:

       .. sourcecode:: http

         HTTP/1.1 200 OK
         Vary: Accept
         Content-Type: text/javascript

         {
            "ecreation": "2020-04-25 21:42:57.094493",
            "ecreator": {
                "display_name": "Diego Amador",
                "email": "diego.amador@upr.edu",
                "roleid": 3,
                "type": "Professor",
                "uid": 2
            },
            "edescription": "Meeting to discuss plans for integration phase.",
            "eend": "2020-08-05 17:41:00",
            "eid": 1,
            "estart": "2020-08-05 15:41:00",
            "estatus": "active",
            "estatusdate": "2020-04-25 21:44:00.365692",
            "etitle": "Alpha Code Team Meeting",
            "photourl": "https://images.pexels.com/photos/256541/pexels-photo-256541.jpeg",
            "room": {
                "building": {
                    "babbrev": "S",
                    "bcommonname": "STEFANI",
                    "bid": 1,
                    "bname": "LUIS A STEFANI (INGENIERIA)",
                    "btype": "Academico",
                    "distinctfloors": [1,2,3,4,5,6,7],
                    "numfloors": 7,
                    "photourl": null
                },
                "photourl": null,
                "raltitude": 50.04,
                "rcode": "123A1",
                "rcustodian": "naydag.santiago@upr.edu",
                "rdept": "INGENIERIA ELECTRICA",
                "rdescription": "CAPSTONE",
                "rfloor": 1,
                "rid": 56,
                "rlatitude": 50.04,
                "rlongitude": 50.04,
                "roccupancy": 0
            },
            "tags": [
                {"tid": 6,"tname": "ARTE"},
                {"tid": 42,"tname": "FILO"},
                {"tid": 54,"tname": "ICOM"},
                {"tid": 64,"tname": "INSO"}
            ],
            "websites": [
                {
                    "url": "http://ece.uprm.edu/~fvega/",
                    "wdescription": "Our clients webpage",
                    "wid": 2
                }
            ]
         }

       :reqheader Cookie: Must contain session token to authenticate.
       :resheader Content-Type: application/json
       :statuscode 200: no error
       :statuscode 404: Event does not exist
       """
    if request.method == 'GET':
        return EventHandler().getEventByID(eid=eid)
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route(route_prefix + "/App/Events/eid=<int:eid>/Interaction", methods=['GET'])
@user_role_required
def getEventByIDWithInteractions(eid):
    """
          .. py:decorator:: user_role_required

          Uses :func:`~app.handlers.EventHandler.EventHandler.getEventByIDWithInteraction`

          Get Event By ID, and include the user's interactions with it (if any).

          .. :quickref: Event; Get Event By bid with user's interaction

          :param eid: Event ID
          :type eid: int
          :return: JSON

          **Example request**:

          .. sourcecode:: http

            GET /API/App/Events/eid=1/Interaction HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

          **Example response**:

          .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: text/javascript

            {
               "ecreation": "2020-04-25 21:42:57.094493",
               "ecreator": {
                   "display_name": "Diego Amador",
                   "email": "diego.amador@upr.edu",
                   "roleid": 3,
                   "type": "Professor",
                   "uid": 2
               },
               "edescription": "Meeting to discuss plans for integration phase.",
               "eend": "2020-08-05 17:41:00",
               "eid": 1,
               "estart": "2020-08-05 15:41:00",
               "estatus": "active",
               "estatusdate": "2020-04-25 21:44:00.365692",
               "etitle": "Alpha Code Team Meeting",
               "itype": "unfollowed",
               "photourl": "https://images.pexels.com/photos/256541/pexels-photo-256541.jpeg",
               "recommendstatus": "N",
               "room": {
                   "building": {
                       "babbrev": "S",
                       "bcommonname": "STEFANI",
                       "bid": 1,
                       "bname": "LUIS A STEFANI (INGENIERIA)",
                       "btype": "Academico",
                       "distinctfloors": [1,2,3,4,5,6,7],
                       "numfloors": 7,
                       "photourl": null
                   },
                   "photourl": null,
                   "raltitude": 50.04,
                   "rcode": "123A1",
                   "rcustodian": "naydag.santiago@upr.edu",
                   "rdept": "INGENIERIA ELECTRICA",
                   "rdescription": "CAPSTONE",
                   "rfloor": 1,
                   "rid": 56,
                   "rlatitude": 50.04,
                   "rlongitude": 50.04,
                   "roccupancy": 0
               },
               "tags": [
                   {"tid": 6,"tname": "ARTE"},
                   {"tid": 42,"tname": "FILO"},
                   {"tid": 54,"tname": "ICOM"},
                   {"tid": 64,"tname": "INSO"}
               ],
               "websites": [
                   {
                       "url": "http://ece.uprm.edu/~fvega/",
                       "wdescription": "Our clients webpage",
                       "wid": 2
                   }
               ]
            }

          :reqheader Cookie: Must contain session token to authenticate.
          :resheader Content-Type: application/json
          :statuscode 200: no error
          :statuscode 404: Event does not exist
          """
    if request.method == 'GET':
        return EventHandler().getEventByIDWithInteraction(eid=eid, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/CAT/timestamp=<string:timestamp>", methods=['GET'])
@user_role_required
def getEventsCreatedAfterTimestamp(timestamp):
    """
              .. py:decorator:: user_role_required

              Uses :func:`~app.handlers.EventHandler.EventHandler.getEventsCreatedAfterTimestamp`

              Get Events created after the submitted timestamp.

              .. :quickref: Event; Get events created after timestamp

              :param timestamp: ISO formatted timestamp
              :type timestamp: str
              :return: JSON

              **Example request**:

              .. sourcecode:: http

                GET /API/App/Events/CAT/timestamp=2020-01-30%2000:00:00 HTTP/1.1
                Host: inthenou.uprm.edu
                Accept: application/json

              **Example response**:

              .. sourcecode:: http

                HTTP/1.1 200 OK
                Vary: Accept
                Content-Type: text/javascript

                {
                    "events": [
                        {
                            "eid": 4,
                            "tags": [
                                {"tid": 1,"tname": "ADMI"},
                                {"tid": 2,"tname": "ADOF"},
                                {"tid": 3,"tname": "AGRO"},
                                {"tid": 4,"tname": "ALEM"},
                                {"tid": 5,"tname": "ANTR"},
                                {"tid": 6,"tname": "ARTE"}
                            ]
                        },
                        {
                            "eid": 6,
                            "tags": [
                                {"tid": 1,"tname": "ADMI"},
                                {"tid": 2,"tname": "ADOF"},
                                {"tid": 3,"tname": "AGRO"},
                                {"tid": 4,"tname": "ALEM"},
                                {"tid": 5,"tname": "ANTR"},
                                {"tid": 6,"tname": "ARTE"},
                                {"tid": 7,"tname": "ASTR"}
                            ]
                        },
                        {
                            "eid": 7,
                            "tags": [
                                {"tid": 1,"tname": "ADMI"},
                                {"tid": 2,"tname": "ADOF"},
                                {"tid": 3,"tname": "AGRO"},
                                {"tid": 4,"tname": "ALEM"},
                                {"tid": 5,"tname": "ANTR"},
                                {"tid": 6,"tname": "ARTE"}
                            ]
                        }
                    ]
                }

              :reqheader Cookie: Must contain session token to authenticate.
              :resheader Content-Type: application/json
              :statuscode 200: no error
              :statuscode 400: Invalid Timestamp
              """
    if request.method == 'GET':
        return EventHandler().getEventsCreatedAfterTimestamp(timestamp=timestamp, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/Create", methods=['POST'])
@event_creator_role_required
def createEvent():
    """
    .. py:decorator:: event_creator_role_required

    Uses :func:`~app.handlers.EventHandler.EventHandler.createEvent`

    Create an event

    .. :quickref: Event; Create Event

    :return: JSON

    **Example request**:

    .. sourcecode:: http

        POST /API/App/Events/Create HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

    **Body of Request**:

    .. code-block:: json

        {
            "roomid": 5,
            "etitle": "Test Event",
            "edescription": "A test event to see the insert route working.",
            "estart":"2020-10-26 15:40:00",
            "eend": "2020-10-26 16:40:00",
            "photourl": "https://link.to.fake.photo.com/fake-foto.jpg",
            "tags": [
                {"tid": 1},
                {"tid": 2},
                {"tid": 3},
                {"tid": 4},
                {"tid": 5},
                {"tid": 6}
            ],
            "websites": [
                {
                    "url": "https://firstwebsite.com",
                    "wdescription": "my  favorite website"
                },
                {
                    "url": "https://secondsite.net",
                    "wdescription": "my  worst website"
                },
                {
                    "url": "https://thirdsite.edu",
                    "wdescription": null
                }
            ]
        }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 201 CREATED
        Vary: Accept
        Content-Type: text/javascript

        {"eid": 17}



    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Event Created Successfully
    :statuscode 400: Invalid parameter sent.
    """
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return EventHandler().createEvent(json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/Deleted/New/timestamp=<string:timestamp>", methods=['GET'])
@user_role_required
def getNewDeletedEvents(timestamp):
    """
              .. py:decorator:: user_role_required

              Uses :func:`~app.handlers.EventHandler.EventHandler.getNewDeletedEvents`

              Get Events deleted after the submitted timestamp.

              .. :quickref: Event; Get events deleted after timestamp

              :param timestamp: ISO formatted timestamp
              :type timestamp: str
              :return: JSON

              **Example request**:

              .. sourcecode:: http

                GET /API/App/Events/Deleted/New/timestamp=2020-01-30%2000:00:00 HTTP/1.1
                Host: inthenou.uprm.edu
                Accept: application/json


              :reqheader Cookie: Must contain session token to authenticate.
              :resheader Content-Type: application/json
              :statuscode 200: no error
              :statuscode 400: Invalid Timestamp
              """
    if request.method == 'GET':
        return EventHandler().getNewDeletedEvents(timestamp=timestamp)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/eid=<int:eid>/Follow", methods=['POST'])
@user_role_required
def followEvent(eid):
    """
    .. py:decorator:: user_role_required

    Uses :func:`~app.handlers.EventHandler.EventHandler.setInteraction`

    Follow an event.

    .. :quickref: Event; Follow an event.

    :param eid: Event ID
    :type eid: int
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        POST /API/App/Events/eid=1/Follow HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json


    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Followed Successfully
    :statuscode 404: Event does not exist.
    """
    if request.method == 'POST':
        return EventHandler().setInteraction(eid=eid, uid=int(current_user.id), itype="following")
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/eid=<int:eid>/Dismiss", methods=['POST'])
@user_role_required
def dismissEvent(eid):
    """
    .. py:decorator:: user_role_required

    Uses :func:`~app.handlers.EventHandler.EventHandler.setInteraction`

    Dismiss an event.

    .. :quickref: Event; Dismiss an event.

    :param eid: Event ID
    :type eid: int
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        POST /API/App/Events/eid=1/Dismiss HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json


    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Dismissed event successfully
    :statuscode 404: Event does not exist.
    """
    if request.method == 'POST':
        return EventHandler().setInteraction(eid=eid, uid=int(current_user.id), itype="dismissed")
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/eid=<int:eid>/Unfollow", methods=['POST'])
@user_role_required
def unfollowEvent(eid):
    """
    .. py:decorator:: user_role_required

    Uses :func:`~app.handlers.EventHandler.EventHandler.setInteraction`

    Unfollow an event.

    .. :quickref: Event; Unfollow an event.

    :param eid: Event ID
    :type eid: int
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        POST /API/App/Events/eid=1/Unfollow HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json


    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Unfollowed Successfully
    :statuscode 404: Event does not exist.
    """
    if request.method == 'POST':
        return EventHandler().setInteraction(eid=eid, uid=int(current_user.id), itype="unfollowed")
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/eid=<int:eid>/estatus=<string:estatus>", methods=['POST'])
@event_creator_role_required
def setEventStatus(eid, estatus):
    """
    .. py:decorator:: event_creator_role_required

    Uses :func:`~app.handlers.EventHandler.EventHandler.setEventStatus`

    Set an existing event's status as either "active" or "deleted"

    .. :quickref: Event; Set event status.

    :param eid: Event ID
    :type eid: int
    :param estatus: New event status.
    :type estatus: str
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        POST /API/App/Events/eid=1/estatus=deleted HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json


    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Event Status set Successfully
    :statuscode 400: Bad estatus.
    """
    if request.method == 'POST':
        # Todo: verify after merging to Dev. that this does not cause errors.
        list_of_valid_users = (UserHandler().getUsersThatCanModifyEvent(eid=eid, no_json=True))
        if list_of_valid_users is None :
            return jsonify({"eid":eid}),201
        else:
            for user in list_of_valid_users:
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
        
        is_user_issuer = UserHandler().getUserIssuers(id= current_user.id,uid=ecreator, no_json=True)
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
    """
    .. py:decorator:: user_role_required

    Uses :func:`~app.handlers.BuildingHandler.BuildingHandler.getBuildingByID`

    Get Building By ID

    .. :quickref: Building; Get Building By bid

    :param bid: Building ID
    :type bid: int
    :return: JSON

    **Example request**:

    .. sourcecode:: http

      GET /API/App/Buildings/bid=1 HTTP/1.1
      Host: inthenou.uprm.edu
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      {
        "babbrev": "S",
        "bcommonname": "STEFANI",
        "bid": 1,
        "bname": "LUIS A STEFANI (INGENIERIA)",
        "btype": "Academico",
        "distinctfloors": [1,2,3,4,5,6,7]
        "numfloors": 7,
        "photourl": null
      }

    :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 404: Building does not exist
    """
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



@app.route(route_prefix + "/App/Tags", methods=['GET'])
def getAllTags():
    if request.method == 'GET':
        try:
            #Check for session 
            if current_user.id:
                print(str(current_user.id))
                return TagHandler().getAllTags()
            
        except:
            #No session Found
            #Check for token in Json body
                try:
                    #TODO Make this check for token dynamically 
                    if str(request.headers['Token']) == 'This_is_a_token':
                        
                        return TagHandler().getAllTags()
                    else:
                        return jsonify(Error="Try loggin in first "), 401
                except: 
                #No Token found
                    return jsonify(Error="Try loggin in first "), 401
        
        return jsonify(Error="Try loggin in first "), 401   
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

# TODO: verify audit function is working
@app.route(route_prefix + "/Dashboard/Tags/Create", methods=['POST'])
@admin_role_required
def createTag():
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return TagHandler().createTags(jsonTags=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/Dashboard/Tags/tid=<int:tid>/Edit", methods=['POST'])
@admin_role_required
def editTagName(tid):
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return TagHandler().editTagName(tid=tid, json=request.json, uid=int(current_user.id))

    else:
        return jsonify(Error="Method not allowed."), 405
