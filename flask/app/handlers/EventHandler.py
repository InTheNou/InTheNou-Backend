from flask import jsonify
from psycopg2 import IntegrityError
from datetime import datetime
from app.DAOs.EventDAO import EventDAO
from app.handlers.RoomHandler import RoomHandler
from app.handlers.TagHandler import TagHandler
from app.handlers.UserHandler import UserHandler
from app.handlers.WebsiteHandler import WebsiteHandler
import app.handlers.SharedValidationFunctions as SVF

CREATEEVENTKEYS = ['roomid', 'etitle', 'edescription', 'estart', 'eend', 'photourl', 'tags', 'websites']
ESTATUS_TYPES = ['active', 'deleted']
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
ITYPES = ["following", "unfollowed", "dismissed"]
RECOMMENDATION_TYPES = ["R", "N"]
SEARCHSTRING = 'searchstring'
TIMESTAMP = 'timestamp'


def _buildCoreEventResponse(event_tuple):
    """
    Private Method to build core event dictionary to be JSONified.

    :param event_tuple: response tuple from SQL query
    :returns Dict: Event information.
    """
    response = {}
    response['eid'] = event_tuple[0]
    response['ecreator'] = event_tuple[1]
    response['room'] = RoomHandler().safeGetRoomByID(rid=event_tuple[2])
    response['etitle'] = event_tuple[3]
    response['edescription'] = event_tuple[4]
    response['estart'] = str(event_tuple[5])
    response['eend'] = str(event_tuple[6])
    response['ecreation'] = str(event_tuple[7])
    response['estatus'] = event_tuple[8]
    response['estatusdate'] = str(event_tuple[9])
    response['photourl'] = event_tuple[10]
    return response


def _buildEventResponse(event_tuple):
    """
    Private Method to build event dictionary to be JSONified.

    :param event_tuple: response tuple from SQL query
    :returns Dict: Event information..
    """
    response = {}
    response['eid'] = event_tuple[0]

    # This SHOULD not break, since every event SHOULD have a user.
    response['ecreator'] = UserHandler().getUserByID(uid=event_tuple[1], no_json=True)
    response['room'] = RoomHandler().safeGetRoomByID(rid=event_tuple[2])
    response['etitle'] = event_tuple[3]
    response['edescription'] = event_tuple[4]
    response['estart'] = str(event_tuple[5])
    response['eend'] = str(event_tuple[6])
    response['ecreation'] = str(event_tuple[7])
    response['estatus'] = event_tuple[8]
    response['estatusdate'] = str(event_tuple[9])
    response['photourl'] = event_tuple[10]
    response['tags'] = TagHandler().safeGetTagsByEventID(eid=event_tuple[0])
    response['websites'] = WebsiteHandler().getWebistesByEventID(eid=event_tuple[0], no_json=True)
    return response


def _buildTinyEventResponse(event_tuple):
    """
    Private Method to build tiny event dictionary to be JSONified.

    :param event_tuple: response tuple from SQL query
    :returns Dict: Event information.
    """
    response = {}
    response['eid'] = event_tuple[0]
    response['estart'] = str(event_tuple[5])
    response['eend'] = str(event_tuple[6])
    response['ecreation'] = str(event_tuple[7])
    response['estatus'] = event_tuple[8]
    response['estatusdate'] = str(event_tuple[9])
    return response


def _validateEventParameters(json, uid):
    """
    Private method to validate the parameters passed via JSON to create an event.

    :param json: JSON used to create event.
    :param uid: User ID of person trying to create the event.
    :raises: ValueError
    """
    if not isinstance(uid, int) or uid <= 0:
        raise ValueError("ecreator uid value not valid: " + str(uid))
    if not isinstance(json['roomid'], int) or json['roomid'] <= 0:
        raise ValueError("roomid value not valid: " + str(json['roomid']))
    if not isinstance(json['etitle'], str) or json['etitle'].isspace() or json['etitle'] == '':
        raise ValueError("etitle value not valid: " + str(json['etitle']))
    if not isinstance(json['edescription'], str) or json['edescription'].isspace() or json['edescription'] == '':
        raise ValueError("edescription value not valid: " + str(json['edescription']))
    if not isinstance(json['estart'], str) or not _validateTimestamp(datestring=json['estart']):
        raise ValueError("estart value not valid: " + str(json['estart']))
    if not isinstance(json['eend'], str) or not _validateTimestamp(datestring=json['eend']):
        raise ValueError("eend value not valid: " + str(json['eend']))
    if not _validateStartEndDates(start=json['estart'], end=json['eend']):
        raise ValueError(
            "eend [{end}] must be greater than estart [{start}]".format(end=json['eend'], start=json['estart']))
    if json['photourl'] is not None:
        if not isinstance(json['photourl'], str) or json['photourl'].isspace() or json['photourl'] == '':
            raise ValueError("photourl value not valid: " + str(json['photourl']))
    if not isinstance(json['tags'], list):
        raise ValueError("Array of tags provided improperly: " + str(json['tags']))
    if json['websites'] is not None:
        if not isinstance(json['websites'], list):
            raise ValueError("Array of websites provided improperly: " + str(json['websites']))


def _validateItype(itype):
    """
    Validates itype.

    :param itype: type of interaction
    :return: bool
    """
    if itype not in ITYPES:
        return False
    return True


def _validateTimestamp(datestring):
    """
    Validates timestamp

    :param: datestring
    :return: bool
    :raises: ValueError
    """
    try:
        if datestring != datetime.strptime(datestring, DATETIME_FORMAT).strftime(DATETIME_FORMAT):
            raise ValueError
        return True
    except ValueError:
        return False


def _validateStartEndDates(start, end):
    """
    Validate that Event Start time is not less than the end time.

    :param start: Start timestamp
    :param end: end timestamp
    :return: bool
    """
    if datetime.strptime(start, DATETIME_FORMAT) < datetime.strptime(end, DATETIME_FORMAT):
        return True
    return False


def _validate_uid_eid(uid, eid):
    """
    Validate that a User ID and Event ID are integers.

    :param uid: User ID
    :param eid: Event ID
    :raises: ValueError
    """
    if not isinstance(uid, int) or uid < 0:
        raise ValueError("Invalid uid: " + str(uid))
    if not isinstance(eid, int) or eid < 0:
        raise ValueError("Invalid eid: " + str(eid))


class EventHandler:
    """
    Handler Class to manage getting/creating/modifying events and event-user interactions.
    """
    # todo: extract all/most of hardcoded key names to variables.

    def createEvent(self, json, uid):
        """Attempt to create an event.

        :param uid: User ID.
        :type uid: int
        :param json: JSON object with the following keys:

                * roomid
                * etitle
                * edescription
                * estart
                * eend
                * photourl
                * websites
                * tags

        :type json: JSON
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        for key in CREATEEVENTKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
        try:
            _validateEventParameters(json=json, uid=uid)
            tags = TagHandler().unpackTags(json_tags=json['tags'])
            WebsiteHandler().validateWebsites(list_of_websites=json['websites'])
        except ValueError as e:
            return jsonify(Error=str(e)), 400
        except KeyError as ke:
            return jsonify(Error="Missing Key in JSON: " + str(ke)), 400

        if len(tags) < 3 or len(tags) > 10:
            return jsonify(Error="Improper number of unique tags provided: " + str(len(tags))), 400

        dao = EventDAO()
        eid = dao.createEvent(ecreator=uid, roomid=json['roomid'], etitle=json['etitle'],
                              edescription=json['edescription'], estart=json['estart'],
                              eend=json['eend'], photourl=json['photourl'], tags=tags,
                              websites=json['websites'])
        try:
            eid = eid[0]
        except TypeError:
            return jsonify(Error=str(eid)), 400

        return jsonify({"eid": eid}), 201

    def getAllDeletedEventsSegmented(self, offset, limit=20):
        """Get all events that have been marked as deleted.

                :param offset: Number of results to skip from top of list.
                :type offset: int
                :param limit: Number of results to return. Default = 20.
                :type limit: int
                :returns JSON Response Object: JSON Response Object containing success or error response.
                """
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400
        dao = EventDAO()
        events = dao.getAllDeletedEventsSegmented(offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            event_list = []
            for row in events:
                event_entry = _buildCoreEventResponse(event_tuple=row)
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getAllEventsSegmented(self, offset, limit=20):
        """Get all events.

           :param offset: Number of results to skip from top of list.
           :type offset: int
           :param limit: Number of results to return. Default = 20.
           :type limit: int
           :returns JSON Response Object: JSON Response Object containing success or error response.
           """
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400
        dao = EventDAO()
        events = dao.getAllEventsSegmented(offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            event_list = []
            for row in events:
                event_entry = _buildCoreEventResponse(event_tuple=row)
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getAllPastEventsSegmented(self, offset, limit=20):
        """Get all events whose end dates are equal to or less than the current timestamp of the database.

           :param offset: Number of results to skip from top of list.
           :type offset: int
           :param limit: Number of results to return. Default = 20.
           :type limit: int
           :returns JSON Response Object: JSON Response Object containing success or error response.
           """
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400
        dao = EventDAO()
        events = dao.getAllPastEventsSegmented(offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            event_list = []
            for row in events:
                event_entry = _buildCoreEventResponse(event_tuple=row)
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getEventByID(self, eid, no_json=False):
        """Return the event entry belonging to the specified eid.

        :param eid: Event ID
        :type eid: int
        :param no_json: States whether or not to return the successful response as a dictionary.
        :type no_json: bool
        :returns JSON Response Object: JSON Response Object containing success or error response.
        """
        if not isinstance(eid, int) or not eid > 0:
            return jsonify(Error="Invalid eid: " + str(eid)), 400
        dao = EventDAO()
        event = dao.getEventByID(eid)
        if not event:
            return jsonify(Error='Event does not exist: eid=' + str(eid)), 404
        else:
            response = _buildEventResponse(event_tuple=event)
            if no_json:
                return response
            return jsonify(response)

    def getEventByIDWithInteraction(self, eid, uid):
        """Return the event entry belonging to the specified eid, plus the user interaction entry for the given uid.

        :param eid: Event ID
        :type eid: int
        :param uid: User ID
        :type uid: int
        :returns JSON Response Object: json response with event IDs and tags for each event.
        """
        if not isinstance(uid, int) or not uid > 0:
            return jsonify(Error="Invalid uid: " + str(uid)), 400
        if not isinstance(eid, int) or not eid > 0:
            return jsonify(Error="Invalid eid: " + str(eid)), 400

        event_response = self.getEventByID(eid=eid, no_json=True)

        # If it's not a dictionary, it is an error JSON.
        if not isinstance(event_response, dict):
            return event_response

        # TODO: consider moving this to User Handler/Dao
        user_interaction = EventDAO().getEventInteractionByUserID(eid=eid, uid=uid)

        # If no interaction found, object is None; replace with None tuple
        if not user_interaction:
            user_interaction = [None, None]

        event_response["itype"] = user_interaction[0]
        event_response["recommendstatus"] = user_interaction[1]

        return jsonify(event_response)

    def getEventsCreatedAfterTimestamp(self, timestamp, uid):
        """
        Get the upcoming active event IDs that a user has not interacted with,
        along with the tags for that event.

        :param timestamp: ISO formatted timestamp string. ("%Y-%m-%d %H:%M:%S")
        :type timestamp: str
        :param uid: the user's ID.
        :type uid: int
        :returns JSON Response Object: json response with event IDs and tags for each event.
        """
        if not isinstance(timestamp, str) or not _validateTimestamp(datestring=timestamp):
            return jsonify(Error='Invalid timestamp: ' + str(timestamp)), 400
        if not isinstance(uid, int) or not uid > 0:
            return jsonify(Error="Invalid uid: " + str(uid)), 400

        dao = EventDAO()
        event_ids = dao.getEventIDsCreatedAfterTimestamp(uid=uid, timestamp=timestamp)
        if not event_ids:
            response = {'events': None}
        else:
            event_list = []
            for row in event_ids:
                event_entry = {"eid": row[0], "tags": TagHandler().safeGetTagsByEventID(eid=row[0])}
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getEventsCreatedByUser(self, uid, offset, limit=20):
        """Return the events created by a given user, specified by offset and limit parameters.

        :param uid: User ID
        :type uid: int
        :param offset: Number of result rows to ignore from top of query results.
        :type offset: int
        :param limit: Max number of result rows to return. Default=20.
        :type limit: int
        :returns JSON Response Object: JSON containing limit-defined number of events created by a user.
        """
        if not isinstance(uid, int) or not uid > 0:
            return jsonify(Error="Invalid uid: " + str(uid)), 400
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400

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

    def getDismissedEvents(self, uid, offset, limit=20):
        """Return the dismissed event entries specified by offset and limit parameters.

        :param uid: User ID
        :type uid: int
        :param offset: Number of result rows to ignore from top of query results.
        :type offset: int
        :param limit: Max number of result rows to return. Default=20.
        :type limit: int
        :returns JSON Response Object: JSON containing limit-defined number of events dismissed by a user.
        """
        if not isinstance(uid, int) or not uid > 0:
            return jsonify(Error="Invalid uid: " + str(uid)), 400
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400

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

    def getNewDeletedEvents(self, timestamp):
        """
        Get a list of the core information for events deleted at or after the given timestamp.

        :param timestamp: Time used to look for events that have been deleted at or after. ("%Y-%m-%d %H:%M:%S")
        :type timestamp: str
        :returns JSON Response Object: JSON containing limit-defined number of events dismissed by a user.
        """
        if not isinstance(timestamp, str) or not _validateTimestamp(datestring=timestamp):
            return jsonify(Error='Invalid timestamp: ' + str(timestamp)), 400
        dao = EventDAO()
        events = dao.getNewDeletedEvents(timestamp=timestamp)
        if not events:
            response = {'events': None}
        else:
            event_list = []
            for row in events:
                event_entry = _buildTinyEventResponse(event_tuple=row)
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getPastFollowedEventsSegmented(self, uid, offset, limit=20):
        """Return the user's followed event entries that have ended, specified by offset and limit parameters.

        :param uid: User ID
        :type uid: int
        :param offset: Number of result rows to ignore from top of query results.
        :type offset: int
        :param limit: Max number of result rows to return. Default=20.
        :type limit: int
        :returns JSON Response Object: JSON containing limit-defined number of events followed by a user that have ended.
        """
        if not isinstance(uid, int) or not uid > 0:
            return jsonify(Error="Invalid uid: " + str(uid)), 400
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400

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

    def getUpcomingFollowedEventsSegmented(self, uid, offset, limit=20):
        """Return the upcoming, active, followed event entries specified by offset and limit parameters.

        :param uid: User ID
        :type uid: int
        :param offset: Number of result rows to ignore from top of query results.
        :type offset: int
        :param limit: Max number of result rows to return. Default=20.
        :type limit: int
        :returns JSON Response Object: JSON containing limit-defined number of events followed by a user that have not ended.
        """
        if not isinstance(uid, int) or not uid > 0:
            return jsonify(Error="Invalid uid: " + str(uid)), 400
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400

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

    def getUpcomingGeneralEventsSegmented(self, uid, offset, limit=20):
        """Return the upcoming, active event entries specified by offset and limit parameters.

        :param uid: User ID
        :type uid: int
        :param offset: Number of result rows to ignore from top of query results.
        :type offset: int
        :param limit: Max number of result rows to return. Default=20.
        :type limit: int
        :returns JSON Response Object: JSON containing limit-defined number of events that have not ended.
        """
        if not isinstance(uid, int) or not uid > 0:
            return jsonify(Error="Invalid uid: " + str(uid)), 400
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400

        dao = EventDAO()
        events = dao.getUpcomingGeneralEventsSegmented(uid=uid, offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            event_list = []
            for row in events:
                event_entry = _buildCoreEventResponse(event_tuple=row)
                # TODO: Consider reworking generalEventsSegmented and builder.
                event_entry['itype'] = row[11]
                event_entry['recommendstatus'] = row[12]
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getUpcomingGeneralEventsByKeywordsSegmented(self, uid, searchstring, offset, limit=20):
        """Return the upcoming, active event entries specified by offset and limit parameters.

        :param uid: User ID
        :type uid: int
        :param searchstring: String to use as search criteria for general events. Search terms must be separated by whitespaces.
        :type searchstring: str
        :param offset: Number of result rows to ignore from top of query results.
        :type offset: int
        :param limit: Max number of result rows to return. Default=20.
        :type limit: int
        :returns JSON Response Object: JSON containing limit-defined number of events that have not ended and match search criteria.
        """
        if not isinstance(uid, int) or not uid > 0:
            return jsonify(Error="Invalid uid: " + str(uid)), 400
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
            # Process keywords to be filtered and separated by pipes.
            keywords = SVF.processSearchString(searchstring=searchstring)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400

        dao = EventDAO()
        events = dao.getUpcomingGeneralEventsByKeywordsSegmented(uid=uid, keywords=keywords, offset=offset, limit=limit)
        if not events:
            response = {'events': None}
        else:
            event_list = []
            for row in events:
                event_entry = _buildCoreEventResponse(event_tuple=row)
                # TODO: Consider reworking generalEventsSegmented and builder.
                event_entry['itype'] = row[11]
                event_entry['recommendstatus'] = row[12]
                event_list.append(event_entry)
            response = {'events': event_list}
        return jsonify(response)

    def getUpcomingRecommendedEventsSegmented(self, uid, offset, limit=20):
        """Return the upcoming, active, recommended event entries specified by offset and limit parameters.

        :param uid: User ID
        :type uid: int
        :param offset: Number of result rows to ignore from top of query results.
        :type offset: int
        :param limit: Max number of result rows to return. Default=20.
        :type limit: int
        :returns JSON Response Object: JSON containing limit-defined number of events recommended to a user that have not ended.
        """
        if not isinstance(uid, int) or not uid > 0:
            return jsonify(Error="Invalid uid: " + str(uid)), 400
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400

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

    def getUpcomingRecommendedEventsByKeywordSegmented(self, uid, searchstring, offset, limit=20):
        """Return the upcoming, recommended, active event entries specified by offset and limit parameters.

        :param uid: User ID
        :type uid: int
        :param searchstring: String to use as search criteria for recommended events. Search terms must be separated by whitespaces.
        :type searchstring: str
        :param offset: Number of result rows to ignore from top of query results.
        :type offset: int
        :param limit: Max number of result rows to return. Default=20.
        :type limit: int
        :returns JSON Response Object: JSON containing limit-defined number of recommended events that have not ended and match search criteria.
        """
        if not isinstance(uid, int) or not uid > 0:
            return jsonify(Error="Invalid uid: " + str(uid)), 400
        try:
            SVF.validate_offset_limit(offset=offset, limit=limit)
            # Process keywords to be filtered and separated by pipes.
            keywords = SVF.processSearchString(searchstring=searchstring)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400

        dao = EventDAO()
        events = dao.getUpcomingRecommendedEventsByKeywordSegmented(uid=uid, keywords=keywords, offset=offset,
                                                                    limit=limit)
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

    def setEventStatus(self, uid, eid, estatus):
        """Set the estatus of an event entry to the specified value.

        :param uid: User ID
        :type uid: int
        :param eid: Event ID.
        :type eid: int
        :param estatus: New status for event. Current Accepted statuses: ['active', 'deleted']
        :type estatus: str
        :returns JSON Response Object: JSON containing successful post response.
        """
        try:
            _validate_uid_eid(uid=uid, eid=eid)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400
        if not isinstance(estatus, str) or estatus not in ESTATUS_TYPES:
            return jsonify(Error='Invalid estatus = ' + str(estatus)), 400
        # TODO: During integration, add user verification from Diego's Handlers.
        # if userCanModifyEvent(uid, eid)

        dao = EventDAO()
        uid_eid_pair = dao.setEventStatus(eid=eid, estatus=estatus)
        try:
            return jsonify({"eid": uid_eid_pair[0]}), 201
        except TypeError:
            return jsonify(Error=str(uid_eid_pair)), 400

    def setInteraction(self, uid, eid, itype):
        """Set an eventuserinteractions entry that states the user has interacted with the specified event.

        :param uid: User ID
        :type uid: int
        :param eid: Event ID.
        :type eid: int
        :param itype: type of interaction. Currently accepted interactions: ["following", "unfollowed", "dismissed"]
        :type itype: str
        :returns JSON Response Object: JSON containing post response.
        """
        try:
            _validate_uid_eid(uid=uid, eid=eid)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400
        if not isinstance(itype, str) or not _validateItype(itype=itype):
            return jsonify(Error="Invalid itype: " + str(itype)), 400

        dao = EventDAO()
        result = dao.setInteraction(uid=uid, eid=eid, itype=itype)

        # TODO: Implement a better way to do this error handling.
        try:
            new_usertags = []
            for row in result:
                new_usertags.append(TagHandler().buildCoreUserTagResponse(tag_tuple=row))

            # Calling this within the try block, because if the setInteraction call fails,
            # psql will block all transactions until current one finishes, and will cause
            # a 500 error instead of the intended 400 below.
            event = dao.getEventByID(eid=eid)
            tiny_event = _buildTinyEventResponse(event_tuple=event)

            response = {}
            response['tags'] = new_usertags
            response['event'] = tiny_event
            return jsonify(response), 201
        except TypeError:
            return jsonify(Error=str(result)), 400

    def setRecommendation(self, uid, eid, recommendstatus):
        """Set an eventuserinteractions entry that states if the specified event has been recommended to the user or not.

        :param uid: User ID
        :type uid: int
        :param eid: Event ID.
        :type eid: int
        :param recommendstatus: qualitative result of recommendation calculation. Currently accepted recommendstatus: ["R", "N"]
        :type recommendstatus: str
        :returns JSON Response Object: JSON containing post response.
        """
        try:
            _validate_uid_eid(uid=uid, eid=eid)
        except ValueError as ve:
            return jsonify(Error=str(ve)), 400
        if not isinstance(recommendstatus, str) or recommendstatus not in RECOMMENDATION_TYPES:
            return jsonify(Error='Invalid recommendstatus = ' + str(recommendstatus)), 400

        dao = EventDAO()
        uid_eid_pair = dao.setRecommendation(uid=uid, eid=eid, recommendstatus=recommendstatus)

        try:
            return jsonify({"uid": uid_eid_pair[0],
                            "eid": uid_eid_pair[1]}), 201
        except TypeError:
            return jsonify(Error=str(uid_eid_pair)), 400
