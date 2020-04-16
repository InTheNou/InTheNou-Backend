from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.WebsiteDAO import WebsiteDAO
import validators
SERVICEWEBSITEKEYS = ['Websites']


def _buildCoreWebsiteResponse(website_tuple):
    """
    Private Method to build core event dictionary to be JSONified.
    Parameters:
        event_tuple: response tuple from SQL query
    Returns:
        Dict: Event information.
    """
    response = {}
    response['wid'] = website_tuple[0]
    response['url'] = website_tuple[1]

    return response


def _buildWebsiteResponse(website_tuple):
    response = {}
    response['wid'] = website_tuple[0]
    response['url'] = website_tuple[1]
    response['wdescription'] = website_tuple[2]

    # Verify that changes to schema reflect properly;
    # changes cause following property to be handled externally.
    # response['isdeleted'] = website_tuple[3]
    return response


def _buildInsertWebsiteResponse(website_tuple, url):
    response = {}
    response['wid'] = website_tuple[0]
    response['url'] = url
    response['wdescription'] = website_tuple[3]

    # Verify that changes to schema reflect properly;
    # changes cause following property to be handled externally.
    # response['isdeleted'] = website_tuple[3]
    return response


def _buildWebsiteIDResponse(website_tuple):
    """
    Private Method to build core event dictionary to be JSONified.
    Parameters:
        event_tuple: response tuple from SQL query
    Returns:
        Dict: Event information.
    """
    response = {}
    response['wid'] = website_tuple[0]
    return response


class WebsiteHandler:
    def createWebsite(self, url):
        """
        Creeates a website entry and returns the wid 
        Parameters:
        url: The url of the website to create
        """
        dao = WebsiteDAO()
        websiteID = dao.createWebsite(url=url)
        return _buildWebsiteIDResponse(websiteID)

    def getWebsiteByID(self, wid):
        dao = WebsiteDAO()
        site = dao.getWebsiteByID(wid=wid)
        return _buildWebsiteResponse(site)

    def unpackWebsites(self, json):
        websites = []
        for site in json:
            if site not in websites:
                websites.append(site)

        return websites

    def getWebistesByEventID(self, eid, no_json=False):
        dao = WebsiteDAO()
        sites = dao.getWebsitesByEventID(eid=eid)
        site_list = []
        if not sites:
            site_list = None
        else:
            for row in sites:
                site_list.append(_buildWebsiteResponse(website_tuple=row))
        response = site_list
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
                site_list.append(_buildWebsiteResponse(website_tuple=row))
        response = site_list
        if no_json:
            return response
        return jsonify(response)

    def insertServiceWebsite(self, sid, json):
        """
        """
        for key in SERVICEWEBSITEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400
        handler = WebsiteHandler()

        sites = []
        website = []
        sites = (handler.unpackWebsites(json['Websites']))
        dao = WebsiteDAO()

        if not sites:
            website = None

        else:

            for row in sites:
                print(row)
                if(validators.url(row['url'])):
                    website.append(_buildInsertWebsiteResponse(url=row['url'], website_tuple=dao.insertWebsiteToService(
                        sid=sid, wid=(dao.createWebsite(url=row['url'])), wdescription=row['wdescription'])))

                else:
                    website.append(
                        {"wid": None})

        return jsonify({"Websites":website}),201

    def removeServiceWebsite(self, sid, json):
        """
        """
        for key in SERVICEWEBSITEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400

        handler = WebsiteHandler()
        sites = []
        siteIDs = []
        websiteInfo = []
        sites = (handler.unpackWebsites(json['Websites']))
        dao = WebsiteDAO()

        if not sites:
            websiteInfo = None
        else:
            for x in sites:

                ID = (dao.removeWebsitesGivenServiceID(sid=sid, wid=x['wid']))
                # print('Removed PhoneID '+str(x['phoneid']) + ' from service '+ str(sid))
                if(ID == None):
                    websiteInfo.append(
                        "Website ID not associated with Service-> sid: " + str(sid) + ' Websiteid: ' + (str(x['wid'])))
                else:
                    siteIDs.append(int(ID))
                    # print('Phones deleted IDs: '+ str(phoneIDs))
            for row in siteIDs:
                websiteInfo.append(_buildCoreWebsiteResponse(
                    website_tuple=dao.getWebsiteByID(row)))

        return jsonify(websiteInfo)

    def validateWebsites(self, list_of_websites):
        """
        Validate that a list of json websites consisting of keys "url" and
        "wdescription" are valid strings.
        Raises:
            ValueError
            KeyError
        """
        if list_of_websites:
            for site in list_of_websites:
                if not isinstance(site['url'], str) or site['url'].isspace() or site['url'] == "":
                    raise ValueError("Invalid url value: " + str(site['url']))
                if site['wdescription'] is not None:
                    if not isinstance(site['wdescription'], str) or site['wdescription'].isspace() or site['wdescription'] == "":
                        raise ValueError(
                            "Invalid wdescription value: " + str(site['wdescription']))
