from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.WebsiteDAO import WebsiteDAO


def _buildWebsiteResponse(site_tuple):
    """
    Private Method to build core event dictionary to be JSONified.
    Parameters:
        event_tuple: response tuple from SQL query
    Returns:
        Dict: Event information.
    """
    response = {}
    response['wid'] = site_tuple[0]
    response['url'] = site_tuple[1]
    response['wdescription'] = site_tuple[2]
    response['isdeleted'] = site_tuple[3]
    return response


def _buildWebsiteIDResponse(site_tuple):
    """
    Private Method to build core event dictionary to be JSONified.
    Parameters:
        event_tuple: response tuple from SQL query
    Returns:
        Dict: Event information.
    """
    response = {}
    response['wid'] = site_tuple[0]
    return response

class WebsiteHandler:
    def createWebsite(self,url):
        dao=WebsiteDAO()
        websiteID=dao.createWebsite(url=url)
        return _buildWebsiteIDResponse(websiteID)

    def getWebsiteByID(self,wid):
        dao=WebsiteDAO()
        site=dao.getWebsiteByID(wid=wid)
        return _buildWebsiteResponse(site)


    def unpackWebsites(self, json):
        websites = [] 
        for site in json:
            if site['website'] not in websites:
                websites.append(site['website'])
                
        return websites

    def getWebistesByEventID(self, eid, no_json=False):
        dao = WebsiteDAO()
        sites = dao.getWebsitesByEventID(eid=eid)
        site_list = []
        if not sites:
            site_list = None
        else:
            for row in sites:
                site_list.append(_buildWebsiteResponse(site_tuple=row))
        response = {"websites": site_list}
        if no_json:
            return response
        return jsonify(response)

    def getWebistesByServiceID(self, sid, no_json=False):
        dao = WebsiteDAO()
        sites = dao.getWebsitesByServiceID(sid=sid)
        site_list = []
        if not sites:
            site_list = None
        else:
            for row in sites:
                site_list.append(_buildWebsiteResponse(site_tuple=row))
        response = {"websites": site_list}
        if no_json:
            return response
        return jsonify(response)