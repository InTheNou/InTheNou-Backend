from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.TagDAO import TagDAO


def _buildTagResponse(tag_tuple):
    response = {}
    response['tid'] = tag_tuple[0]
    response['tname'] = tag_tuple[1]
    return response


class TagHandler:

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
            return jsonify(Error='Tag does not exist: ' + str(tid)), 404
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
            return jsonify(Error='Event Tags do not exist: ' + str(eid)), 404
        else:
            tag_list = []
            for row in tags:
                tag_list.append(_buildTagResponse(tag_tuple=row))
            response = {"tags": tag_list}
            if no_json:
                return response
            return jsonify(response)
