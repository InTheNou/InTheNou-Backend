from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.TagDAO import TagDAO


def _buildTagResponse(tag_tuple):
    response = {}
    response['tid'] = tag_tuple[0]
    response['tname'] = tag_tuple[1]
    return response


def _buildWeightedTagResponse(tag_tuple):
    response = {}
    response['tid'] = tag_tuple[0]
    response['tname'] = tag_tuple[1]
    response['tagweight'] = tag_tuple[2]
    return response

def _buildCoreWeightedTagResponse(tag_tuple):
    response = {}
    response['tid'] = tag_tuple[1]
    response['tagweight'] = tag_tuple[2]
    return response


class TagHandler:

    def unpackTags(self, json_tags):
        tags = []
        for tag in json_tags:
            if tag['tid'] not in tags:
                tags.append(tag['tid'])
        return tags

    def buildCoreUserTagResponse(self, tag_tuple):
        response = {}
        response['tid'] = tag_tuple[1]
        response['tagweight'] = tag_tuple[2]
        return response


    def getTagByID(self, tid, no_json=False):
        """
        Return the tag entry belonging to the specified tid.
        Parameters:
            tid: tag ID.
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing tag information. Error JSON otherwise.
        """
        dao = TagDAO()
        tag = dao.getTagByID(tid=tid)
        if not tag:
            return jsonify(Error='Tag does not exist: tid=' + str(tid)), 404
        else:
            response = _buildTagResponse(tag_tuple=tag)
            if no_json:
                return response
            return jsonify(response)

    def getTagsByEventID(self, eid, no_json=False):
        """
        Return the tag entries belonging to an event specified by its eid.
        Parameters:
            eid: Event's ID.
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing Tags belonging to an event. Error JSON otherwise.
        """
        dao = TagDAO()
        tags = dao.getTagsByEventID(eid=eid)
        if not tags:
            return jsonify(Error='Event Tags do not exist: eid=' + str(eid)), 404
        else:
            tag_list = []
            for row in tags:
                tag_list.append(_buildTagResponse(tag_tuple=row))
            response = {"tags": tag_list}
            if no_json:
                return response
            return jsonify(response)

    def safeGetTagsByEventID(self, eid):
        tags = self.getTagsByEventID(eid=eid, no_json=True)["tags"]
        # Following line checks if the above returns a json (no tags found or no_json set to False.
        if not isinstance(tags, list):
            tags = str(tags)
        return tags

    # TODO: Add safe version of this method when needed.
    def getTagsByUserID(self, uid, no_json=False):
        """
        Return the tag entries belonging to a user specified by their uid.
        Parameters:
            uid: User's ID.
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing Tags belonging to an event. Error JSON otherwise.
        """
        dao = TagDAO()
        tags = dao.getTagsByUserID(uid=uid)
        if not tags:
            return jsonify(Error='No Tags Found for User: uid=' + str(uid)), 404
        else:
            tag_list = []
            for row in tags:
                tag_list.append(_buildWeightedTagResponse(tag_tuple=row))
            response = {"tags": tag_list}
            if no_json:
                return response
            return jsonify(response)

    def getAllTags(self, no_json=False):
        """
        Return all tag entries in the database.
        Parameters:
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing all tags. Error JSON otherwise.
        """
        dao = TagDAO()
        tags = dao.getAllTags()
        if not tags:
            return jsonify(Error='Could not find any tags in system.'), 404
        else:
            tag_list = []
            for row in tags:
                tag_list.append(_buildTagResponse(tag_tuple=row))
            response = {"tags": tag_list}
            if no_json:
                return response
            return jsonify(response)

    def setUserTag(self, uid, tid, weight):
        """
        Set/create the weight of the user's tag to the specified value.
        Parameters:
            uid: User ID
            tid: tag ID
            weight: integer representing new weight to set for the tag.
        Returns:
            JSON: containing the updated entry for the user's tag. Error JSON otherwise.
        """
        dao = TagDAO()
        user_tag = dao.setUserTag(uid=uid, tid=tid, weight=weight)
        user_tag_dict = _buildWeightedTagResponse(tag_tuple=user_tag)
        return user_tag_dict

    def batchSetUserTags(self,  json, weight, uid=None, no_json=False):
        """
        Set the weight for the given tags in a JSON to a specified value
        """
        if uid is None:
            uid = json['uid']
        if weight < 0 or weight > 200:
            return jsonify(Error='Tag Weight outside range of 0-200: ' + str(weight)), 400

        tags = self.unpackTags(json_tags=json['tags'])
        updated_usertags = []
        rows = TagDAO().batchSetUserTags(uid=uid, tags=tags, weight=weight)
        try:
            for user_tag in rows:
                updated_usertags.append(_buildCoreWeightedTagResponse(tag_tuple=user_tag))
        except TypeError:
            return jsonify(Error=str(rows)), 400

        response = {"tags": updated_usertags}
        if no_json:
            return response
        return jsonify(response), 201

