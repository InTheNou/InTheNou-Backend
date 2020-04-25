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

    def createTags(self, jsonTags, uid):
        tags = []
        if "Tags" in jsonTags:
            json = jsonTags['Tags']
        else:
            return jsonify(Error="Tag names must be within 'Tags' header"), 401
        for key in json:
            tags.append(key['tname'])

        dao = TagDAO()

        response = []
        for tname in tags:
            response.append(_buildTagResponse(
                dao.createTag(tname=tname, uid=uid)))
        return jsonify(response)

    def editTagName(self, tid, json, uid):
        dao = TagDAO()
        response = []
        tagname = ""
        tagname = str(json['tname'])
        if tagname is not None:
            try:
                tag = dao.editTagName(tid=tid, tname=tagname, uid=uid)
                if tag is not None:
                    response.append(_buildTagResponse(tag))
                    return jsonify(response)
                else:
                    return jsonify(Error="No tag found with provided ID"), 404

            except TypeError:
                return jsonify(Error="Another tag with that name exists"), 400

    def unpackTags(self, json_tags):
        """
        Validate that a list of jsons containing key 'tid' is valid,
        and returns a list of ints of the tid's
        Returns:
            List[int]: List of tid's
        Raises:
            ValueError
            KeyError
        """
        
        tags = []
        for tag in json_tags:
            if 'tid' not in tag:
                raise KeyError("Key not found: tid")
            tid = tag['tid']
            if not isinstance(tid, int) or tid < 0:
                raise ValueError("Invalid tid: " + str(tid))
            if tid not in tags:
                tags.append(tid)
       
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
        if not isinstance(tid, int) or not tid > 0:
            return jsonify(Error="Invalid tid: " + str(tid)), 400
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
        if not isinstance(eid, int) or not eid > 0:
            return jsonify(Error="Invalid eid: " + str(eid)), 400
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

    def getTagsByUserID(self, uid, no_json=False):
        """
        Return the tag entries belonging to a user specified by their uid.
        Parameters:
            uid: User's ID.
            no_json: states if the response should be returned as JSON or not.
        Returns:
            JSON: containing Tags belonging to an event. Error JSON otherwise.
        """
        if not isinstance(uid, int) or not uid > 0:
            return jsonify(Error="Invalid uid: " + str(uid)), 400
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

    # TODO: THIS METHOD IS NOT CURRENTLY USED.
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
        if not isinstance(uid, int) or not uid > 0:
            return jsonify(Error="Invalid uid: " + str(uid)), 400
        if not isinstance(tid, int) or not tid > 0:
            return jsonify(Error="Invalid tid: " + str(tid)), 400
        dao = TagDAO()
        # todo: this method call requires a cursor.
        user_tag = dao.setUserTag(uid=uid, tid=tid, weight=weight)
        user_tag_dict = _buildWeightedTagResponse(tag_tuple=user_tag)
        return user_tag_dict

    def batchSetUserTags(self,  json, weight, uid, no_json=False):
        """
        Set the weight for the given tags in a JSON to a specified value
        """
       
        try:
            # Temporary until Merge with Diego's Code
            if uid is None:
                raise KeyError("UID not provided.")
            if not isinstance(uid, int) or uid <= 0:
                raise ValueError("Invalid uid: " + str(uid))

            if weight < 0 or weight > 200:
                raise ValueError('Tag Weight outside range of 0-200: ' + str(weight))
            if 'tags' not in json:
                raise KeyError("Key not found in JSON: tags")

            tags = self.unpackTags(json_tags=json['tags'])
            
        except ValueError as e:
            return jsonify(Error=str(e)), 400
        except KeyError as e:
            return jsonify(Error=str(e)), 400

        updated_usertags = []
        print(str(tags))
        rows = TagDAO().batchSetUserTags(uid=uid, tags=tags, weight=weight)
        try:
            for user_tag in rows:
                updated_usertags.append(
                    _buildCoreWeightedTagResponse(tag_tuple=user_tag))
        except TypeError:
            return jsonify(Error=str(rows)), 400

        response = {"tags": updated_usertags}
        if no_json:
            print(response)
            return response
        return jsonify(response), 201
