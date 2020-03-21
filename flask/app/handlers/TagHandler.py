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
            JSON: containing room information. Error JSON otherwise.
        """
        dao = TagDAO()
        tag = dao.getTagByID(tid)
        if not tag:
            return jsonify(Error='Tag does not exist: ' + str(tid)), 404
        else:
            response = _buildTagResponse(tag_tuple=tag)
            if no_json:
                return response
            return jsonify(response)
