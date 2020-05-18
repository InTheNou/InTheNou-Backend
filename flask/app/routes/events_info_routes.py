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
from datetime import timedelta,datetime
import base64
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
    .. :quickref: Event; Get Event By bid

    Get Event By ID
    Uses :func:`~app.handlers.EventHandler.EventHandler.getEventByID`

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
            Content-Type: application/json


            {
                "ecreation": "2020-05-01 02:27:01.729007",
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
                "estatusdate": "None",
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
                    {
                        "tid": 6,
                        "tname": "ARTE"
                    },
                    {
                        "tid": 42,
                        "tname": "FILO"
                    },
                    {
                        "tid": 54,
                        "tname": "ICOM"
                    },
                    {
                        "tid": 64,
                        "tname": "INSO"
                    }
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
    :statuscode 403: User is not logged in.
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
    .. :quickref: Event; Get Event By bid with user's interaction

    Get Event By ID, and include the user's interactions with it (if any).
    Uses :func:`~app.handlers.EventHandler.EventHandler.getEventByIDWithInteraction`

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
            Content-Type: application/json


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
    :statuscode 403: User is not logged in.
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
    .. :quickref: Event; Get events created after timestamp

    Get Events created after the submitted timestamp.
    Uses :func:`~app.handlers.EventHandler.EventHandler.getEventsCreatedAfterTimestamp`

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
            Content-Type: application/json


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
    :statuscode 403: User is not logged in.
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
    .. :quickref: Event; Create Event

    Create an event
    Uses :func:`~app.handlers.EventHandler.EventHandler.createEvent`

    :return: JSON

    **Example request**:

        .. sourcecode:: http

            POST /API/App/Events/Create HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Request Body**:

        .. sourcecode:: json

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
            Content-Type: application/json


            {"eid": 17}

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Event Created Successfully
    :statuscode 400: Invalid parameter sent.
    :statuscode 401: User does not have appropriate role to use route.
    :statuscode 403: User is not logged in.
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
    .. :quickref: Event; Get events deleted after timestamp

    Get events that have been deleted after the given timestamp.
    Uses :func:`~app.handlers.EventHandler.EventHandler.getNewDeletedEvents`

    :param timestamp: ISO formatted timestamp
    :type timestamp: str
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Events/Deleted/New/timestamp=2020-01-30%2000:00:00 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "events": [{
                    "ecreation": "2020-05-01 02:27:01.731852",
                    "eend": "2020-10-05 17:41:00",
                    "eid": 3,
                    "estart": "2020-10-05 15:41:00",
                    "estatus": "deleted",
                    "estatusdate": "2020-05-01 02:27:52.770806"
                }]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Invalid Timestamp
    :statuscode 403: User is not logged in.
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
    .. :quickref: Event-User Interaction; Follow an event.

    Follow an event.
    Uses :func:`~app.handlers.EventHandler.EventHandler.setInteraction`

    :param eid: Event ID
    :type eid: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            POST /API/App/Events/eid=2/Follow HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json


            {
                "event": {
                    "ecreation": "2020-05-01 02:27:01.730759",
                    "eend": "2020-09-05 17:41:00",
                    "eid": 2,
                    "estart": "2020-09-05 15:41:00",
                    "estatus": "active",
                    "estatusdate": "None"
                },
                "tags": [
                    {"tagweight": 5,"tid": 42},
                    {"tagweight": 80,"tid": 54},
                    {"tagweight": 5,"tid": 64},
                    {"tagweight": 5,"tid": 73},
                    {"tagweight": 5,"tid": 47},
                    {"tagweight": 5,"tid": 53}
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Followed Successfully
    :statuscode 403: User is not logged in.
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
    .. :quickref: Event-User Interaction; Dismiss an event.

    Dismiss an event.
    Uses :func:`~app.handlers.EventHandler.EventHandler.setInteraction`

    :param eid: Event ID
    :type eid: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            POST /API/App/Events/eid=2/Dismiss HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json


            {
                "event": {
                    "ecreation": "2020-05-01 02:27:01.730759",
                    "eend": "2020-09-05 17:41:00",
                    "eid": 2,
                    "estart": "2020-09-05 15:41:00",
                    "estatus": "active",
                    "estatusdate": "None"
                },
                "tags": [
                    {"tagweight": 0,"tid": 42},
                    {"tagweight": 60,"tid": 54},
                    {"tagweight": 0,"tid": 64},
                    {"tagweight": 0,"tid": 73},
                    {"tagweight": 0,"tid": 47},
                    {"tagweight": 0,"tid": 53}
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Dismissed event successfully
    :statuscode 403: User is not logged in.
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
    .. :quickref: Event-User Interaction; Unfollow an event.

    Unfollow an event.
    Uses :func:`~app.handlers.EventHandler.EventHandler.setInteraction`

    :param eid: Event ID
    :type eid: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            POST /API/App/Events/eid=2/Unfollow HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json


            {
                "event": {
                    "ecreation": "2020-05-01 02:27:01.730759",
                    "eend": "2020-09-05 17:41:00",
                    "eid": 2,
                    "estart": "2020-09-05 15:41:00",
                    "estatus": "active",
                    "estatusdate": "None"
                },
                "tags": [
                    {"tagweight": 0,"tid": 42},
                    {"tagweight": 60,"tid": 54},
                    {"tagweight": 0,"tid": 64},
                    {"tagweight": 0,"tid": 73},
                    {"tagweight": 0,"tid": 47},
                    {"tagweight": 0,"tid": 53}
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Unfollowed Successfully
    :statuscode 403: User is not logged in.
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
    .. :quickref: Event; Set event status.

    Set an existing event's status as either "active" or "deleted".
    Uses :func:`~app.handlers.EventHandler.EventHandler.setEventStatus`

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

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json


            {"eid":1}

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Event Status set Successfully
    :statuscode 400: Bad estatus.
    :statuscode 401: User does not have appropriate role to use route.
    :statuscode 403: User is not logged in.
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


@app.route(route_prefix + "/App/Events/eid=<int:eid>/recommendstatus=<string:recommendstatus>", methods=['POST'])
@user_role_required
def setRecommendation(eid, recommendstatus):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Event-User Interaction; Set Recommendation.

    Set the recommendation status of an event for the user.
    Uses :func:`~app.handlers.EventHandler.EventHandler.setRecommendation`

    :param eid: Event ID
    :type eid: int
    :param recommendstatus: Recommendation Status.
    :type recommendstatus: str
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            POST /API/App/Events/eid=1/recommendstatus=R HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json


            {"eid":3,"uid":1}

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Posted recommendation successfully.
    :statuscode 400: Invalid recommendstatus.
    :statuscode 403: User is not logged in.
    :statuscode 404: Event does not exist.
    """
    if request.method == 'POST':
        return EventHandler().setRecommendation(eid=eid, uid=int(current_user.id), recommendstatus=recommendstatus)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/Created/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getEventsCreatedByUser(offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Event; Get Events created by current user.

    Get a list of events created by the logged in user.
    Uses :func:`~app.handlers.EventHandler.EventHandler.getEventsCreatedByUser`

    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Events/Created/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "events": [
                    {
                        "ecreation": "2020-05-01 03:51:46.116066",
                        "ecreator": 1,
                        "edescription": "A test event to see the insert route working.",
                        "eend": "2020-10-26 16:40:00",
                        "eid": 12,
                        "estart": "2020-04-30 23:51:46",
                        "estatus": "active",
                        "estatusdate": "None",
                        "etitle": "Test Event",
                        "photourl": null,
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
                            "rcode": "122",
                            "rcustodian": "isidoro.courvetier@upr.edu",
                            "rdept": "INGENIERIA ELECTRICA",
                            "rdescription": "LABORATORIO DE COMPUTADORA",
                            "rfloor": 1,
                            "rid": 54,
                            "rlatitude": 50.04,
                            "rlongitude": 50.04,
                            "roccupancy": 0
                        }
                    },
                    {
                        "ecreation": "2020-05-01 03:51:46.311287",
                        "ecreator": 1,
                        "edescription": "A test event to see the insert route working.",
                        "eend": "2020-10-26 16:40:00",
                        "eid": 13,
                        "estart": "2020-04-30 23:51:46",
                        "estatus": "active",
                        "estatusdate": "None",
                        "etitle": "Test Event",
                        "photourl": null,
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
                            "rcode": "123A",
                            "rcustodian": "naydag.santiago@upr.edu",
                            "rdept": "INGENIERIA ELECTRICA",
                            "rdescription": "POWER ELECTRONIC",
                            "rfloor": 1,
                            "rid": 55,
                            "rlatitude": 50.04,
                            "rlongitude": 50.04,
                            "roccupancy": 0
                        }
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return EventHandler().getEventsCreatedByUser(uid=int(current_user.id), offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/Dismissed/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getDismissedEvents(offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Event; Get Events dismissed by current user.

    Get a list of events dismissed by the logged in user.
    Uses :func:`~app.handlers.EventHandler.EventHandler.getDismissedEvents`

    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Events/Dismissed/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "events": [
                    {
                        "ecreation": "2020-05-01 02:27:01.730759",
                        "ecreator": 3,
                        "edescription": "Meeting to discuss more plans for integration phase.",
                        "eend": "2020-09-05 17:41:00",
                        "eid": 2,
                        "estart": "2020-09-05 15:41:00",
                        "estatus": "active",
                        "estatusdate": "None",
                        "etitle": "Alpha Code Team Meeting 2",
                        "photourl": null,
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
                        }
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return EventHandler().getDismissedEvents(uid=int(current_user.id), offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/Following/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getUpcomingFollowedEventsSegmented(offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Event; Get upcoming events current user is following.

    Get a list of upcoming events that have been followed by the logged in user.
    Uses :func:`~app.handlers.EventHandler.EventHandler.getUpcomingFollowedEventsSegmented`

    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Events/Following/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "events": [
                    {
                        "ecreation": "2020-05-01 02:27:01.730759",
                        "ecreator": 3,
                        "edescription": "Meeting to discuss more plans for integration phase.",
                        "eend": "2020-09-05 17:41:00",
                        "eid": 2,
                        "estart": "2020-09-05 15:41:00",
                        "estatus": "active",
                        "estatusdate": "None",
                        "etitle": "Alpha Code Team Meeting 2",
                        "photourl": null,
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
                        }
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return EventHandler().getUpcomingFollowedEventsSegmented(uid=int(current_user.id), offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/General/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getUpcomingGeneralEventsSegmented(offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Event; Get upcoming events.

    Get a list of upcoming events.
    Uses :func:`~app.handlers.EventHandler.EventHandler.getUpcomingGeneralEventsSegmented`

    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Events/General/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "events": [
                    {
                        "ecreation": "2020-05-01 02:27:01.730759",
                        "ecreator": 3,
                        "edescription": "Meeting to discuss more plans for integration phase.",
                        "eend": "2020-09-05 17:41:00",
                        "eid": 2,
                        "estart": "2020-09-05 15:41:00",
                        "estatus": "active",
                        "estatusdate": "None",
                        "etitle": "Alpha Code Team Meeting 2",
                        "photourl": null,
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
                        }
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return EventHandler().getUpcomingGeneralEventsSegmented(uid=int(current_user.id), offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/General/search=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getUpcomingGeneralEventsByKeywordsSegmented(searchstring, offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Event; Get upcoming events by keywords.

    Get a list of upcoming events that are matched with the searchstring.
    Uses :func:`~app.handlers.EventHandler.EventHandler.getUpcomingGeneralEventsByKeywordsSegmented`

    :param searchstring: space-separated string of keywords to use for search of events.
    :type searchstring: str
    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Events/General/search=test%20event/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "events": [
                    {
                        "ecreation": "2020-05-01 02:27:01.730759",
                        "ecreator": 3,
                        "edescription": "Meeting to discuss more plans for integration phase.",
                        "eend": "2020-09-05 17:41:00",
                        "eid": 2,
                        "estart": "2020-09-05 15:41:00",
                        "estatus": "active",
                        "estatusdate": "None",
                        "etitle": "Alpha Code Team Meeting 2",
                        "photourl": null,
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
                        }
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return EventHandler().getUpcomingGeneralEventsByKeywordsSegmented(uid=int(current_user.id),
                                                                          searchstring=searchstring,
                                                                          offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/History/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getPastFollowedEventsSegmented(offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Event; Get past followed events.

    Get a list of events that have ended and the current user has followed (user's history).
    Uses :func:`~app.handlers.EventHandler.EventHandler.getPastFollowedEventsSegmented`

    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Events/History/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "events": [
                    {
                        "ecreation": "2020-05-01 02:27:01.730759",
                        "ecreator": 3,
                        "edescription": "Meeting to discuss more plans for integration phase.",
                        "eend": "2020-09-05 17:41:00",
                        "eid": 2,
                        "estart": "2020-09-05 15:41:00",
                        "estatus": "active",
                        "estatusdate": "None",
                        "etitle": "Alpha Code Team Meeting 2",
                        "photourl": null,
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
                        }
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return EventHandler().getPastFollowedEventsSegmented(uid=int(current_user.id), offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/Recommended/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getUpcomingRecommendedEventsSegmented(offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Event; Get upcoming recommended events.

    Get a list of upcoming events that have been recommended to the current user.
    Uses :func:`~app.handlers.EventHandler.EventHandler.getUpcomingRecommendedEventsSegmented`

    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Events/Recommended/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "events": [
                    {
                        "ecreation": "2020-05-01 02:27:01.730759",
                        "ecreator": 3,
                        "edescription": "Meeting to discuss more plans for integration phase.",
                        "eend": "2020-09-05 17:41:00",
                        "eid": 2,
                        "estart": "2020-09-05 15:41:00",
                        "estatus": "active",
                        "estatusdate": "None",
                        "etitle": "Alpha Code Team Meeting 2",
                        "photourl": null,
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
                        }
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return EventHandler().getUpcomingRecommendedEventsSegmented(uid=int(current_user.id),
                                                                    offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Events/Recommended/search=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getUpcomingRecommendedEventsByKeywordSegmented(searchstring, offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Event; Get upcoming recommended events by keywords.

    Get a list of upcoming events that have been recommended to the user and are matched with the searchstring.
    Uses :func:`~app.handlers.EventHandler.EventHandler.getUpcomingRecommendedEventsByKeywordSegmented`

    :param searchstring: space-separated string of keywords to use for search of events.
    :type searchstring: str
    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Events/Recommended/search=test%20event/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "events": [
                    {
                        "ecreation": "2020-05-01 02:27:01.730759",
                        "ecreator": 3,
                        "edescription": "Meeting to discuss more plans for integration phase.",
                        "eend": "2020-09-05 17:41:00",
                        "eid": 2,
                        "estart": "2020-09-05 15:41:00",
                        "estatus": "active",
                        "estatusdate": "None",
                        "etitle": "Alpha Code Team Meeting 2",
                        "photourl": null,
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
                        }
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return EventHandler().getUpcomingRecommendedEventsByKeywordSegmented(uid=int(current_user.id),
                                                                             searchstring=searchstring,
                                                                             offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/Dashboard/Events/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@mod_role_required
def getAllEventsSegmented(offset, limit):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Event; Get all events segmented.

    Get a list of all events.
    Uses :func:`~app.handlers.EventHandler.EventHandler.getAllEventsSegmented`

    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/Dashboard/Events/offset=0/limit=1 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "events": [
                    {
                        "ecreation": "2020-05-01 02:27:01.730759",
                        "ecreator": 3,
                        "edescription": "Meeting to discuss more plans for integration phase.",
                        "eend": "2020-09-05 17:41:00",
                        "eid": 2,
                        "estart": "2020-09-05 15:41:00",
                        "estatus": "active",
                        "estatusdate": "None",
                        "etitle": "Alpha Code Team Meeting 2",
                        "photourl": null,
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
                        }
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 401: User does not have appropriate role to use route.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return EventHandler().getAllEventsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/Dashboard/Events/ecreator=<int:ecreator>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@mod_role_required
def getEventsCreatedByOtherUser(ecreator, offset, limit):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Event; Get events created by other user.

    Get a list of events created by another user.
    Uses :func:`~app.handlers.UserHandler.UserHandler.getUserIssuers` &
    :func:`~app.handlers.EventHandler.EventHandler.getEventsCreatedByUser`

    :param ecreator: User ID of whom the events are being searched.
    :type ecreator: int
    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/Dashboard/Events/ecreator=2/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "events": [
                    {
                        "ecreation": "2020-05-01 02:27:01.729007",
                        "ecreator": 2,
                        "edescription": "Meeting to discuss plans for integration phase.",
                        "eend": "2020-08-05 17:41:00",
                        "eid": 1,
                        "estart": "2020-08-05 15:41:00",
                        "estatus": "active",
                        "estatusdate": "2020-05-01 03:51:48.110718",
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
                        }
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 401: User does not have appropriate role to use route.
    :statuscode 403: User is not logged in.
    """
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
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Event; Get all deleted events segmented.

    Get a list of all deleted events.
    Uses :func:`~app.handlers.EventHandler.EventHandler.getAllDeletedEventsSegmented`

    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/Dashboard/Events/Deleted/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "events": [
                    {
                        "ecreation": "2020-05-01 02:27:01.729007",
                        "ecreator": 2,
                        "edescription": "Meeting to discuss plans for integration phase.",
                        "eend": "2020-08-05 17:41:00",
                        "eid": 1,
                        "estart": "2020-08-05 15:41:00",
                        "estatus": "active",
                        "estatusdate": "2020-05-01 03:51:48.110718",
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
                        }
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 401: User does not have appropriate role to use route.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return EventHandler().getAllDeletedEventsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/Dashboard/Events/Past/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@mod_role_required
def getAllPastEventsSegmented(offset, limit):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Event; Get all past events segmented.

    Get a list of all events whose end time is less than or equal to the current timestamp.
    Uses :func:`~app.handlers.EventHandler.EventHandler.getAllPastEventsSegmented`

    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/Dashboard/Events/Past/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "events": [
                    {
                        "ecreation": "2020-05-01 02:27:01.729007",
                        "ecreator": 2,
                        "edescription": "Meeting to discuss plans for integration phase.",
                        "eend": "2020-08-05 17:41:00",
                        "eid": 1,
                        "estart": "2020-08-05 15:41:00",
                        "estatus": "active",
                        "estatusdate": "2020-05-01 03:51:48.110718",
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
                        }
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 401: User does not have appropriate role to use route.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return EventHandler().getAllPastEventsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Rooms/rid=<int:rid>", methods=['GET'])
@user_role_required
def getRoomByID(rid):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Room; Get room by ID.

    Get a room entry by ID.
    Uses :func:`~app.handlers.RoomHandler.RoomHandler.getRoomByID`

    :param rid: Room ID.
    :type rid: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Rooms/rid=42 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
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
                "rcode": "114D",
                "rcustodian": "fabio.andrade@ece.uprm.edu ",
                "rdept": "INGENIERIA ELECTRICA",
                "rdescription": "LABORATORIO INVESTIGACION DR. FABIO ANDRADE ",
                "rfloor": 1,
                "rid": 42,
                "rlatitude": 50.04,
                "rlongitude": 50.04,
                "roccupancy": 0,
                "services": []
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 400: Bad offset/limit values.
    """
    if request.method == 'GET':
        return RoomHandler().getRoomByID(rid=rid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Rooms/babbrev=<string:babbrev>/rcode=<string:rcode>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getRoomsByCodeSearchSegmented(babbrev, rcode, offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Room; Get room by room code.

    Get a list of rooms that match a search by room code, which consists of the
    building abbreviation and room number.
    Uses :func:`~app.handlers.RoomHandler.RoomHandler.getRoomsByCodeSearchSegmented`

    :param babbrev: Building abbreviation.
    :type babbrev: str
    :param rcode: Building room number/code.
    :type rcode: str
    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Rooms/babbrev=S/rcode=123/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "rooms": [
                    {
                        "building": {
                            "babbrev": "S",
                            "bid": 1,
                            "bname": "LUIS A STEFANI (INGENIERIA)"
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
                    {
                        "building": {
                            "babbrev": "S",
                            "bid": 1,
                            "bname": "LUIS A STEFANI (INGENIERIA)"
                        },
                        "photourl": null,
                        "raltitude": 50.04,
                        "rcode": "123A",
                        "rcustodian": "naydag.santiago@upr.edu",
                        "rdept": "INGENIERIA ELECTRICA",
                        "rdescription": "POWER ELECTRONIC",
                        "rfloor": 1,
                        "rid": 55,
                        "rlatitude": 50.04,
                        "rlongitude": 50.04,
                        "roccupancy": 0
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 400: Bad offset/limit values.
    """
    if request.method == 'GET':
        return RoomHandler().getRoomsByCodeSearchSegmented(babbrev=babbrev, rcode=rcode, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Rooms/searchstring=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getRoomsByKeywordSegmented(searchstring, offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Room; Get room by keywords.

    Get a list of rooms that match a search by keywords.
    Uses :func:`~app.handlers.RoomHandler.RoomHandler.getRoomsByKeywordSegmented`

    :param searchstring: space-separated keywords to search the room descriptions.
    :type searchstring: str
    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Rooms/searchstring=capstone/offset=0/limit=2 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "rooms": [
                    {
                        "building": {
                            "babbrev": "S",
                            "bid": 1,
                            "bname": "LUIS A STEFANI (INGENIERIA)"
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
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 400: Bad offset/limit values.
    """
    if request.method == 'GET':
        return RoomHandler().getRoomsByKeywordSegmented(searchstring=searchstring, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Rooms/bid=<int:bid>/rfloor=<int:rfloor>", methods=['GET'])
@user_role_required
def getRoomsByBuildingAndFloor(bid, rfloor):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Room; Get room by building and floor.

    Get a list of all rooms that belong to a given building's given floor.
    Uses :func:`~app.handlers.RoomHandler.RoomHandler.getRoomsByBuildingAndFloor`

    :param bid: Building ID.
    :type bid: int
    :param rfloor: Floor of building to search.
    :type rfloor: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Rooms/bid=1/rfloor=3 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Shortened example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
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
                "rooms": [
                    {
                        "photourl": null,
                        "raltitude": 50.04,
                        "rcode": "300",
                        "rcustodian": "victor.ramirez2@upr.edu",
                        "rdept": "COLEGIO DE INGENIERIA",
                        "rdescription": "OFICINA DEL CUSTODIO DE LAS LLAVES",
                        "rfloor": 3,
                        "rid": 170,
                        "rlatitude": 50.04,
                        "rlongitude": 50.04,
                        "roccupancy": 0
                    },
                    {
                        "photourl": null,
                        "raltitude": 50.04,
                        "rcode": "301",
                        "rcustodian": "jose.colom1@upr.edu",
                        "rdept": "INGENIERIA ELECTRICA",
                        "rdescription": "ALMACEN",
                        "rfloor": 3,
                        "rid": 171,
                        "rlatitude": 50.04,
                        "rlongitude": 50.04,
                        "roccupancy": 0
                    },
                    {
                        "photourl": null,
                        "raltitude": 50.04,
                        "rcode": "302",
                        "rcustodian": "agustin.rullan@upr.edu",
                        "rdept": "COLEGIO DE INGENIERIA",
                        "rdescription": "COBACHA",
                        "rfloor": 3,
                        "rid": 172,
                        "rlatitude": 50.04,
                        "rlongitude": 50.04,
                        "roccupancy": 0
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad bid/rfloor values.
    :statuscode 403: User is not logged in.
    :statuscode 404: No rooms found for given building ID and floor number.
    """
    if request.method == 'GET':
        return RoomHandler().getRoomsByBuildingAndFloor(bid=bid, rfloor=rfloor)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Buildings/bid=<int:bid>", methods=['GET'])
@user_role_required
def getBuildingByID(bid):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Building; Get Building By bid

    Get Building By ID
    Uses :func:`~app.handlers.BuildingHandler.BuildingHandler.getBuildingByID`

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
            Content-Type: application/json

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
    :statuscode 403: User is not logged in.
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
    """
    .. py:decorator:: user_role_required
    .. :quickref: Building; Get all buildings.

    Get a list of all buildings in the system.
    Uses :func:`~app.handlers.BuildingHandler.BuildingHandler.getAllBuildings`

    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/Dev/Buildings HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "buildings": [
                    {
                        "babbrev": "S",
                        "bcommonname": "STEFANI",
                        "bid": 1,
                        "bname": "LUIS A STEFANI (INGENIERIA)",
                        "btype": "Academico",
                        "distinctfloors": [1,2,3,4,5,6,7],
                        "numfloors": 7,
                        "photourl": null
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return BuildingHandler().getAllBuildings()
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Buildings/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getAllBuildingsSegmented(offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Building; Get all buildings segmented.

    Get a list of some buildings in the system.
    Uses :func:`~app.handlers.BuildingHandler.BuildingHandler.getAllBuildingsSegmented`

    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Buildings/offset=0/limit=1 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            "buildings":
            [
                {
                    "babbrev": "S",
                    "bcommonname": "STEFANI",
                    "bid": 1,
                    "bname": "LUIS A STEFANI (INGENIERIA)",
                    "btype": "Academico",
                    "distinctfloors": [1,2,3,4,5,6,7],
                    "numfloors": 7,
                    "photourl": null
                }
            ]

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return BuildingHandler().getAllBuildingsSegmented(offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


# Automated test not set up
@app.route(route_prefix + "/App/Buildings/Search/searchstring=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getBuildingsByKeywords(searchstring, offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Building; Get all buildings by keywords.

    Get a list of buildings in the system that match the searchstring.
    Uses :func:`~app.handlers.BuildingHandler.BuildingHandler.getBuildingsByKeyword`

    :param searchstring: space-separated keywords to search the buildings.
    :type searchstring: str
    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Buildings/Search/searchstring=luis/offset=0/limit=1 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            "buildings":
            [
                {
                    "babbrev": "S",
                    "bcommonname": "STEFANI",
                    "bid": 1,
                    "bname": "LUIS A STEFANI (INGENIERIA)",
                    "btype": "Academico",
                    "distinctfloors": [1,2,3,4,5,6,7],
                    "numfloors": 7,
                    "photourl": null
                }
            ]

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return BuildingHandler().getBuildingsByKeyword(keyword=searchstring,
                                                       offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Services/searchstring=<string:searchstring>/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@user_role_required
def getServicesByKeywords(searchstring, offset, limit):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Service; Get services by keywords.

    Get a list of services in the system that match the searchstring.
    Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.getServicesByKeywords`

    :param searchstring: space-separated keywords to search the services.
    :type searchstring: str
    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Services/searchstring=fernando/offset=0/limit=1 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "services": [
                    {
                        "numbers": [
                            {
                                "phoneid": 3,
                                "pnumber": "787-832-4040,5842",
                                "ptype": "E"
                            }
                        ],
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
                            "rcode": "229A",
                            "rcustodian": "jfernando.vega@upr.edu",
                            "rdept": "INGENIERIA ELECTRICA",
                            "rdescription": "OFICINA PROFESOR DR. FERNANDO VEGA ",
                            "rfloor": 2,
                            "rid": 151,
                            "rlatitude": 50.04,
                            "rlongitude": 50.04,
                            "roccupancy": 0
                        },
                        "sdescription": "Office Hours to discuss class topics, and consult with Capstone Team.",
                        "sid": 3,
                        "sname": "Office Hours: Fernando Vega",
                        "sschedule": "L: 3:30pm - 4:30pm, W: 1:30pm - 3:30pm",
                        "websites": [
                            {
                                "url": "http://ece.uprm.edu/~fvega/",
                                "wdescription": "J. Fernando Vega-Riveros, Ph.D. Professor",
                                "wid": 2
                            }
                        ]
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad offset/limit values.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return ServiceHandler().getServicesByKeywords(searchstring=searchstring, offset=offset, limit=limit)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Tags", methods=['GET'])
def getAllTags():
    """
    Uses :func:`~app.handlers.TagHandler.TagHandler.getAllTags`
    .. :quickref: Tag; Get all tags.

    Get all tags in the system. This route requires the user to
    either be logged in with a session, or to posses a
    server-issued token.

    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Tags HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Shortened example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "tags": [
                    {
                        "tid": 1,
                        "tname": "ADMI"
                    },
                    {
                        "tid": 2,
                        "tname": "ADOF"
                    },
                    {
                        "tid": 3,
                        "tname": "AGRO"
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :reqheader Token: If request does not contain session,
        it must contain a token header.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 401: User is not logged in and does not posses a valid Token
    """
    if request.method == 'GET':
        try:
            #Check for session 
            if current_user.id:
                print(str(current_user.id))
                return TagHandler().getAllTags()
            
        except:
            #No session Found
            #Check for token in Json body
                # try:
                    #TODO Make this check for token dynamically 
                    token = str(request.headers['Token'])
                    token = base64.b64decode(bytes(token, 'utf-8'))
                    token = token.decode('utf-8')
                    tokenDate = (datetime.strptime(token, '%Y-%m-%d %H:%M:%S.%f'))    
                    currentDate= datetime.now()
                    print("Current date :"+ str(currentDate)+" token date: "+str(tokenDate))
                    date_diff = (currentDate - tokenDate)/timedelta(minutes=1)
                    print (date_diff)
                    if (date_diff) < 5:
                        return TagHandler().getAllTags()
                    else:
                        return jsonify(Error="Try loggin in first "), 401
                # except: 
                # #No Token found
                #     return jsonify(Error="Try loggin in first "), 401
        
        return jsonify(Error="Try loggin in first "), 401   
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Tags/eid=<int:eid>", methods=['GET'])
@user_role_required
def getTagsByEventID(eid):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Tag; Get an event's tags.

    Get a list of all the tags associated with a given event.
    Uses :func:`~app.handlers.TagHandler.TagHandler.getTagsByEventID`

    :param eid: Event ID
    :type eid: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Tags/eid=1 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "tags": [
                    {
                        "tid": 42,
                        "tname": "FILO"
                    },
                    {
                        "tid": 47,
                        "tname": "GEOL"
                    },
                    {
                        "tid": 53,
                        "tname": "HUMA"
                    },
                    {
                        "tid": 54,
                        "tname": "ICOM"
                    },
                    {
                        "tid": 64,
                        "tname": "INSO"
                    },
                    {
                        "tid": 73,
                        "tname": "METE"
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 400: Bad eid value.
    :statuscode 403: User is not logged in.
    :statuscode 404: Event does not exist in system.
    """
    if request.method == 'GET':
        return TagHandler().getTagsByEventID(eid=eid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Tags/tid=<int:tid>", methods=['GET'])
@user_role_required
def getTagByID(tid):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Tag; Get tag by ID.

    Get a tag by its ID.
    Uses :func:`~app.handlers.TagHandler.TagHandler.getTagByID`

    :param tid: Tag ID
    :type tid: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Tags/tid=1 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "tid": 1,
                "tname": "ADMI"
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 404: Tag does not exist in system/string passed as tid value.
    """
    if request.method == 'GET':
        return TagHandler().getTagByID(tid=tid)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Tags/UserTags", methods=['GET'])
@user_role_required
def getTagsByUserIDSession():
    """
    .. py:decorator:: user_role_required
    .. :quickref: Tag; Get user's tags/weights.

    Get the current user's tags and tag weights.
    Uses :func:`~app.handlers.TagHandler.TagHandler.getTagsByUserID`

    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Tags/UserTags HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json

            {
                "tags": [
                    {
                        "tagweight": 100,
                        "tid": 1,
                        "tname": "ADMI"
                    },
                    {
                        "tagweight": 100,
                        "tid": 2,
                        "tname": "ADOF"
                    },
                    {
                        "tagweight": 100,
                        "tid": 3,
                        "tname": "AGRO"
                    },
                    {
                        "tagweight": 100,
                        "tid": 4,
                        "tname": "ALEM"
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return TagHandler().getTagsByUserID(uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/App/Tags/User/Remove", methods=['POST'])
@user_role_required
def setUserTagsToZero():
    """
    .. py:decorator:: user_role_required
    .. :quickref: Tag; Remove user tags.

    Set the current user's specified tags to a weight of 0.
    Uses :func:`~app.handlers.TagHandler.TagHandler.batchSetUserTags`

    :return: JSON

    **Example request**:

        .. sourcecode:: http

            POST /API/App/Tags/User/Remove HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Body of Request**:

        .. code-block:: json

            {
                "tags": [
                    {"tid": 1},
                    {"tid": 2},
                    {"tid": 3},
                    {"tid": 4},
                    {"tid": 5}
                    ]
            }

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json

            {
                "tags": [
                    {
                        "tagweight": 0,
                        "tid": 1
                    },
                    {
                        "tagweight": 0,
                        "tid": 2
                    },
                    {
                        "tagweight": 0,
                        "tid": 3
                    },
                    {
                        "tagweight": 0,
                        "tid": 4
                    },
                    {
                        "tagweight": 0,
                        "tid": 5
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Tags successfully set to 0.
    :statuscode 400: Invalid JSON parameters.
    :statuscode 403: User is not logged in.
    """
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
    """
    .. py:decorator:: user_role_required
    .. :quickref: Tag; Add user tags.

    Set the current user's specified tags to a weight of 100.
    Uses :func:`~app.handlers.TagHandler.TagHandler.batchSetUserTags`

    :return: JSON

    **Example request**:

        .. sourcecode:: http

            POST /API/App/Tags/User/Add HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Body of Request**:

        .. code-block:: json

            {
                "tags": [
                    {"tid": 1},
                    {"tid": 2},
                    {"tid": 3},
                    {"tid": 4},
                    {"tid": 5}
                    ]
            }

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json

            {
                "tags": [
                    {
                        "tagweight": 100,
                        "tid": 1
                    },
                    {
                        "tagweight": 100,
                        "tid": 2
                    },
                    {
                        "tagweight": 100,
                        "tid": 3
                    },
                    {
                        "tagweight": 100,
                        "tid": 4
                    },
                    {
                        "tagweight": 100,
                        "tid": 5
                    }
                ]
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Tags successfully set to 100.
    :statuscode 400: Invalid JSON parameters.
    :statuscode 403: User is not logged in.
    """
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
    """
    .. py:decorator:: admin_role_required
    .. :quickref: Tag; Create tags.

    Create new tags.
    Uses :func:`~app.handlers.TagHandler.TagHandler.createTags`

    :return: JSON

    **Example request**:

        .. sourcecode:: http

            POST /API/Dashboard/Tags/Create HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Body of Request**:

        .. code-block:: json

            {
                "Tags": [
                    {"tname": "tag1"},
                    {"tname": "tag2"}
                    ]
            }

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json

            [
                {
                    "tid": 88,
                    "tname": "tag1"
                },
                {
                    "tid": 89,
                    "tname": "tag2"
                }
            ]

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Tags successfully created.
    :statuscode 400: Invalid JSON parameters.
    :statuscode 401: User does not have appropriate role to use route.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return TagHandler().createTags(jsonTags=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/Dashboard/Tags/tid=<int:tid>/Edit", methods=['POST'])
@admin_role_required
def editTagName(tid):
    """
    .. py:decorator:: admin_role_required
    .. :quickref: Tag; Edit tag name.

    Edit an existing tag's name.
    Uses :func:`~app.handlers.TagHandler.TagHandler.editTagName`

    :return: JSON

    **Example request**:

        .. sourcecode:: http

            POST /API/Dashboard/Tags/tid=2/Edit HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Body of Request**:

        .. code-block:: json

            {"tname": "newName"}

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json

            "tags":  [
                {
                    "tid": 2,
                    "tname": "newName"
                }
                    ]

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Tags successfully set to 100.
    :statuscode 400: Invalid JSON parameters.
    :statuscode 401: User does not have appropriate role to use route.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return TagHandler().editTagName(tid=tid, json=request.json, uid=int(current_user.id))

    else:
        return jsonify(Error="Method not allowed."), 405


@app.route(route_prefix + "/Dashboard/Building/Add", methods=['POST'])
@admin_role_required
def addFullBuilding():
    """
    .. py:decorator:: admin_role_required
    .. :quickref: Building; Add building.

    Add a new building to the system or update an existing building.
    Uses :func:`~app.handlers.BuildingHandler.BuildingHandler.addFullBuilding`

    :return: JSON

    **Example request**:

        .. sourcecode:: http

            POST /API/Dashboard/Building/Add HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Body of Request**:

        .. code-block:: json

            {
                "edificioid": "110",
                "nomoficial": "LUIS A STEFANI (INGENIERIA) ",
                "blddenom": "STEFANI",
                "codigoold": "S",
                "bldtype": "1",
                "attributes": [
                  ["2", "1086122.79"],
                  ["15", "18.20956050211146,-67.13997513055801"],
                  ["24", "109753"],
                  ["25", "115605"],
                  ["1", "7"],
                  ["21", "Hormigon"],
                  ["0", "1958"]
                ]
            }

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json

            {
                "Result": "Building Added successfuly LUIS A STEFANI (INGENIERIA). Old bid = None"
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: Building Successfully added/updated.
    :statuscode 400: Invalid JSON parameters.
    :statuscode 401: User does not have appropriate role to use route.
    :statuscode 403: User is not logged in.
    """
    if request.method == 'POST':
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        return BuildingHandler().addFullBuilding(json=request.json, uid=int(current_user.id))

    else:
        return jsonify(Error="Method not allowed."), 405