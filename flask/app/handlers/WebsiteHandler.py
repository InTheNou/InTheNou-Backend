from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.WebsiteDAO import WebsiteDAO

SERVICEWEBSITEKEYS =['Websites']

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
   
    return response

def _buildCoreWebsiteResponse(website_tuple):
    response = {}
    response['wid'] = website_tuple[0]
    response['wdescription'] = website_tuple[3]
    response['isdeleted'] = website_tuple[2]
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
        response = {"Websites": site_list}
        if no_json:
            return response
        return jsonify(response)

    def insertServiceWebsite(self,sid,json):
        """
        """ 
        for key in SERVICEWEBSITEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
        handler =WebsiteHandler()

        
        sites=[]
        website= []
        sites= (handler.unpackWebsites(json['Websites']))
        dao =WebsiteDAO()
       
        
        if not sites:
            website = None
        else:
            for row in sites:
              website.append(_buildCoreWebsiteResponse(dao.insertWebsiteToService(sid=sid,wid=(dao.createWebsite(url=row['url'])),wdescription=row['wdescription'])))

        return jsonify(website)

    def removeServiceWebsite(self,sid,json):
        """
        """ 
        for key in SERVICEWEBSITEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
        
        
        handler=WebsiteHandler()
        sites=[]
        website= []
        sites= (handler.unpackWebsites(json['Websites']))
        dao =WebsiteDAO()
       
        if not sites:
            website = None
        else:
            for row in sites:
              website.append(_buildCoreWebsiteResponse(dao.removeWebsitesGivenServiceID(sid=sid,wid=row['wid'])))

        return jsonify(website)
      