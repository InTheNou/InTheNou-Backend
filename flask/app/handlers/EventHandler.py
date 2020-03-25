from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.EventDAO import EventDAO
from app.DAOs.TagDAO import TagDAO
from app.handlers.RoomHandler import RoomHandler
from app.handlers.TagHandler import TagHandler

CREATEEVENTKEYS = ['roomid', 'etitle', 'edescription', 'estart', 'eend', 'photourl', 'tags', 'websites']

def _buildEventResponse(event_tuple):
    """
    Private Method to build event dictionary to be JSONified.
    Parameters:
        event_tuple: response tuple from SQL query
    Returns:
        Dict: Event information.
    """
    response = {}
    response['eid'] = event_tuple[0]

    # TODO: Add user information Once Diego creates routes (uid, name, lastname)
    response['ecreator'] = event_tuple[1]
    response['room'] = RoomHandler().safeGetRoomByID(rid=event_tuple[2])
    response['etitle'] = event_tuple[3]
    response['edescription'] = event_tuple[4]
    response['estart'] = event_tuple[5]
    response['eend'] = event_tuple[6]
    response['ecreation'] = event_tuple[7]
    response['estatus'] = event_tuple[8]
    response['estatusdate'] = event_tuple[9]
    response['photourl'] = event_tuple[10]
    response['tags'] = TagHandler().safeGetTagsByEventID(eid=event_tuple[0])
    return response


def _buildCoreEventResponse(event_tuple):
    """
    Private Method to build core event dictionary to be JSONified.
    Parameters:
        event_tuple: response tuple from SQL query
    Returns:
        Dict: Event information.
    """
    response = {}
    response['eid'] = event_tuple[0]
    response['ecreator'] = event_tuple[1]
    response['room'] = RoomHandler().getCoreRoomByID(rid=event_tuple[2], no_json=True)
    response['etitle'] = event_tuple[3]
    response['edescription'] = event_tuple[4]
    response['estart'] = event_tuple[5]
    response['eend'] = event_tuple[6]
    response['ecreation'] = event_tuple[7]
    response['estatus'] = event_tuple[8]
    response['estatusdate'] = event_tuple[9]
    response['photourl'] = event_tuple[10]
    return response


def _unpackTags(json_tags):
    tags=[]
    for tag in json_tags:
        if tag['tid'] not in tags:
            tags.append(tag['tid'])
    return tags


class EventHandler:

    def getEventByID(self, eid):
        """Return the event entry belonging to the specified eid.
        eid -- event ID.
        """
        dao = EventDAO()
        event = dao.getEventByID(eid)
        if not event:
            return jsonify(Error='Event does not exist: eid=' + str(eid)), 404
        else:
            response = _buildEventResponse(event_tuple=event)
            return jsonify(response)

    def getUpcomingGeneralEventsSegmented(self, uid, offset, limit=10):
        """Return the upcoming, active event entries specified by offset and limit parameters.
        Parameters:
            uid: User ID
            offset: Number of result rows to ignore from top of query results.
            limit: Max number of result rows to return. Default=10.
        Return:
            JSON Response Object: JSON containing limit-defined number of upcoming, active events.
                """
        dao = EventDAO()
        events = dao.getUpcomingGeneralEventsSegmented(uid=uid, offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            print(events)
            event_list = []
            for row in events:
                event_entry = _buildCoreEventResponse(event_tuple=row)
                # TODO: Consider reworking generalEventsSegmented and builder.
                event_entry['interaction'] = {
                    "itype": row[11],
                    "recommendstatus": row[12]
                }
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getUpcomingFollowedEventsSegmented(self, uid, offset, limit=10):
        """Return the upcoming, active, followed event entries specified by offset and limit parameters.
        Parameters:
            uid: User ID
            offset: Number of result rows to ignore from top of query results.
            limit: Max number of result rows to return. Default=10.
        Return:
            JSON Response Object: JSON containing limit-defined number of upcoming, active events.
                """
        dao = EventDAO()
        events = dao.getUpcomingFollowedEventsSegmented(uid=uid, offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            event_list = []
            for row in events:
                # TODO: consider re-developing Response builders for more flexibility.
                event_entry = _buildCoreEventResponse(event_tuple=row)
                event_entry['recommendstatus'] = row[11]
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getDismissedEvents(self, uid, offset, limit=10):
        """Return the dismissed event entries specified by offset and limit parameters.
        Parameters:
            uid: User ID
            offset: Number of result rows to ignore from top of query results.
            limit: Max number of result rows to return. Default=10.
        Return:
            JSON Response Object: JSON containing limit-defined number of dismissed events.
                """
        dao = EventDAO()
        events = dao.getDismissedEvents(uid=uid, offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            event_list = []
            for row in events:
                # TODO: consider re-developing Response builders for more flexibility.
                event_entry = _buildCoreEventResponse(event_tuple=row)
                event_entry['recommendstatus'] = row[11]
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getUpcomingRecommendedEventsSegmented(self, uid, offset, limit=10):
        """Return the upcoming, active, recommended event entries specified by offset and limit parameters.
        Parameters:
            uid: User ID
            offset: Number of result rows to ignore from top of query results.
            limit: Max number of result rows to return. Default=10.
        Return:
            JSON Response Object: JSON containing limit-defined number of upcoming, active events.
                """
        dao = EventDAO()
        events = dao.getUpcomingRecommendedEventsSegmented(uid=uid, offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            event_list = []
            for row in events:
                # TODO: consider re-developing Response builders for more flexibility.
                event_entry = _buildCoreEventResponse(event_tuple=row)
                event_entry['itype'] = row[11]
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getPastFollowedEventsSegmented(self, uid, offset, limit=10):
        """Return the user's followed event entries that have ended, specified by offset and limit parameters.
        Parameters:
            uid: User ID
            offset: Number of result rows to ignore from top of query results.
            limit: Max number of result rows to return. Default=10.
        Return:
            JSON Response Object: JSON containing limit-defined number past, followed events.
                """
        dao = EventDAO()
        events = dao.getPastFollowedEventsSegmented(uid=uid, offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            event_list = []
            for row in events:
                # TODO: consider re-developing Response builders for more flexibility.
                event_entry = _buildCoreEventResponse(event_tuple=row)
                event_entry['recommendstatus'] = row[11]
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getEventsCreatedByUser(self, uid, offset, limit=10):
        """Return the events created by a given user, specified by offset and limit parameters.
        Parameters:
            uid: User ID
            offset: Number of result rows to ignore from top of query results.
            limit: Max number of result rows to return. Default=10.
        Return:
            JSON Response Object: JSON containing limit-defined number of events created by a user.
                """
        dao = EventDAO()
        events = dao.getEventsCreatedByUser(uid=uid, offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            event_list = []
            for row in events:
                # TODO: consider re-developing Response builders for more flexibility.
                event_entry = _buildCoreEventResponse(event_tuple=row)
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def setInteraction(self, uid, eid, itype):
        """Set an eventuserinteractions entry that states the user has interacted with
        the specified event.
        Parameters:
            uid: User ID
            eid: Event ID.
            itype: type of interaction string.
        Return:
            JSON Response Object: JSON containing successful post response.
                """
        dao = EventDAO()
        uid_eid_pair = dao.setInteraction(uid=uid, eid=eid, itype=itype)
        # TODO: Consider a better way to do this error handling.
        try:
            return jsonify({"uid": uid_eid_pair[0],
                            "eid": uid_eid_pair[1]}), 201
        except TypeError:
            return jsonify(Error=str(uid_eid_pair)), 400

    def setRecommendation(self, uid, eid, recommendstatus):
        """Set an eventuserinteractions entry that states if the specified event
        has been recommended to the user or not.
        Parameters:
            uid: User ID
            eid: Event ID.
            recommendstatus: qualitative result of recommendation calculation.
        Return:
            JSON Response Object: JSON containing successful post response.
                """
        if recommendstatus == 'R' or recommendstatus == 'N':
            dao = EventDAO()
            uid_eid_pair = dao.setRecommendation(uid=uid, eid=eid, recommendstatus=recommendstatus)
            # TODO: Consider a better way to do this error handling.
            try:
                return jsonify({"uid": uid_eid_pair[0],
                                "eid": uid_eid_pair[1]}), 201
            except TypeError:
                return jsonify(Error=str(uid_eid_pair)), 400
        return jsonify(Error='Invalid recommendstatus = ' + str(recommendstatus)), 400

    def setEventStatus(self, uid, eid, estatus):
        """Set the estatus of an event entry to the specified value.
        Parameters:
            uid: User ID
            eid: Event ID.
            estatus: status string.
        Return:
            JSON Response Object: JSON containing successful post response.
                """
        # TODO: During integration, add user verification from Diego's Handlers.
        # if userCanModifyEvent(uid, eid)
        if estatus == 'active' or estatus == 'deleted':
            dao = EventDAO()
            uid_eid_pair = dao.setEventStatus(eid=eid, estatus=estatus)
            # TODO: Consider a better way to do this error handling.
            try:
                return jsonify({"eid": uid_eid_pair[0]}), 201
            except TypeError:
                return jsonify(Error=str(uid_eid_pair)), 400
        return jsonify(Error='Unsupported event status = ' + str(estatus)), 400

    def createEvent(self, json, uid=None):
        """Attempt to create an event.
        Parameters:
            uid: User ID.
            json: JSON object with the following keys:
                ecreator, roomid, etitle, edescription, estart, eend, photourl, websites, tags
        Return:
            JSON Response Object: JSON containing success or error response.
        """
        for key in CREATEEVENTKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
        # TODO: pass uid not through json.

        tags = _unpackTags(json_tags=json['tags'])
        if len(tags) < 3 or len(tags) > 10:
            return jsonify(Error="Improper number of unique tags provided: "+ str(len(tags))), 400

        dao = EventDAO()

        # photoid = dao.insertPhoto(photourl=json['photourl'])

        eid = dao.createEvent(ecreator=json['ecreator'], roomid=json['roomid'], etitle=json['etitle'],
                              edescription=json['edescription'], estart=json['estart'],
                              eend=json['eend'], photourl=json['photourl'], tags=tags, websites=json['websites'])
        # try:
        #     eid=eid[0]
        # except TypeError:
        #     return jsonify(Error=str(eid)), 400
        #
        # for tag in tags:
        #     tag_results = TagDAO().tagEvent(eid=eid, tid=tag)
        #     if tag_results != 'successfully tagged event.':
        #         return jsonify(Error="Invalid tag ID provided: " + str(tag)), 400
        #
        # for website in json['websites']:
        #     wid = dao.insertWebsite(url=website['url'], wdescription=website['wdescription'])
        #     try:
        #         wid = wid[0]
        #     except TypeError:
        #         return jsonify(Error="Invalid website: " + str(website)), 400
        #     dao.addWebsitesToEvent(eid=eid, wid=wid)

        return jsonify({"eid": eid}), 201

