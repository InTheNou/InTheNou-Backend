from flask import jsonify
from psycopg2 import IntegrityError
from app.DAOs.WebsiteDAO import WebsiteDAO


import validators
SERVICEWEBSITEKEYS = ['websites']


def _buildCoreWebsiteResponse(website_tuple):
    """
    Private Method to build website dictionary to be JSONified.

    :param website_tuple: response tuple from SQL query
    :returns Dict: Website information with keys:

    .. code-block:: python

        {'wid', 'url'}
    """
    response = {}
    response['wid'] = website_tuple[0]
    response['url'] = website_tuple[1]

    return response


def _buildWebsiteResponse(website_tuple):
    """
    Private Method to build website dictionary to be JSONified.

    :param website_tuple: response tuple from SQL query
    :returns Dict: Website information with keys:

    .. code-block:: python

        {'wid', 'url', 'wdescription'}
    """
    response = {}
    response['wid'] = website_tuple[0]
    response['url'] = website_tuple[1]
    response['wdescription'] = website_tuple[2]

    # Verify that changes to schema reflect properly;
    # changes cause following property to be handled externally.
    # response['isdeleted'] = website_tuple[3]
    return response


def _buildInsertWebsiteResponse(website_tuple, url):
    """
    Private Method to build website dictionary to be JSONified.

    :param website_tuple: response tuple from SQL query
    :param url: link to website
    :returns Dict: Website information with keys:

    .. code-block:: python

        {'wid', 'url', 'wdescription'}
    """
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
    Private Method to build website dictionary to be JSONified.

    :param website_tuple: response tuple from SQL query
    :returns Dict: Website information with keys:

    .. code-block:: python

        {'wid'}
    """
    response = {}
    response['wid'] = website_tuple[0]
    return response


class WebsiteHandler:
    def createWebsite(self, url, uid):
        """
        Attempt to create a website.
        Uses :func:`~app.DAOs.WebsiteDAO.WebsiteDAO.createWebsite` as well as
        :func:`~app.handlers.WebsiteHandler._buildWebsiteIDResponse`

        :param uid: User ID.
        :type uid: int
        :param url: A link to a website
        :type url: string
        :returns JSON Response Object: JSON Response Object containing
            success or error response.
        """
        dao = WebsiteDAO()
        websiteID = dao.createWebsite(url=url, uid=uid)
        return _buildWebsiteIDResponse(websiteID)

    def getWebsiteByID(self, wid):
        """
        Return a website given it's ID.
        Uses :func:`~app.DAOs.WebsiteDAO.WebsiteDAO.getWebsiteByID` as well as
        :func:`~app.handlers.WebsiteHandler._buildWebsiteIDResponse`

        :param wid: Website ID.
        :type wid: int
        :returns JSON Response Object: JSON Response Object containing
            success or error response.
        """
        dao = WebsiteDAO()
        site = dao.getWebsiteByID(wid=wid)
        return _buildWebsiteResponse(site)

    def unpackWebsites(self, json):
        """
        Returns a website dictionary given a website list.

        :param json: Website list with the following keys:

            * url
            * wdescription

        :type json: JSON
        :returns JSON Response Object: JSON Response Object containing
            success or error response.
        """
        websites = []
        for site in json:
            if site not in websites:
                websites.append(site)

        return websites

    def getWebistesByEventID(self, eid, no_json=False):
        """
        Return a list of websites given a event ID
        Uses :func:`~app.DAOs.WebsiteDAO.WebsiteDAO.getWebsitesByEventID` as well as
        :func:`~app.handlers.WebsiteHandler._buildWebsiteResponse`

        :param eid: Event ID.
        :type eid: int
        :param no_json: Indicates if response is returned as JSON or list.
        :type no_json: bool
        :returns JSON Response Object: JSON Response Object containing
            success or error response.
        """
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
        """
        Returns a website list given an Service ID
        Uses :func:`~app.DAOs.WebsiteDAO.WebsiteDAO.getWebsitesByServiceID` as well as
        :func:`~app.handlers.WebsiteHandler._buildWebsiteResponse`

        :param sid: Service ID.
        :type sid: int
        :param no_json: Indicates if response is returned as JSON or list.
        :type no_json: bool
        :returns JSON Response Object: JSON Response Object containing
            success or error response.
        """
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

    def insertServiceWebsite(self, sid, json, uid):
        """
        Insert a list of websites (urls and desriptions) to a given service.
        Uses :func:`~app.DAOs.WebsiteDAO.WebsiteDAO.insertWebsiteToService` as well as:

            * :func:`~app.handlers.WebsiteHandler.WebsiteHandler.unpackWebsites`
            * :func:`~app.handlers.WebsiteHandler._buildWebsiteResponse`

        :param eid: Event ID.
        :type eid: int
        :param json: list of websites wit the keys:

            * Websites

        :type json: array
        :param uid: User ID
        :type uid: int
        :returns JSON Response Object: JSON Response Object containing
            success or error response.
        """
        for key in SERVICEWEBSITEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400

        handler = WebsiteHandler()

        sites = []
        website = []
        sites = (handler.unpackWebsites(json['websites']))
        dao = WebsiteDAO()

        if not sites:
            return jsonify(Error='Missing websites for submission: '), 400

        website = dao.insertWebsiteToService(sites, sid, uid=uid)
        
        try:
            return jsonify(website),201
        except:
            return jsonify(Error="Service with sid: "+sid+" not found"), 401

    def removeServiceWebsite(self, sid, json, uid):
        """
        Remove a list of websites (urls and desriptions) to a given service.
        Uses :func:`~app.DAOs.WebsiteDAO.WebsiteDAO.removeWebsitesGivenServiceID` as well as:

            * :func:`~app.handlers.WebsiteHandler.WebsiteHandler.unpackWebsites`
            * :func:`~app.handlers.WebsiteHandler.WebsiteHandler.getWebsiteByID`
            * :func:`~app.handlers.WebsiteHandler._buildCoreWebsiteResponse`

        :param sid: Service ID.
        :type sid: int
        :param json: list of websites wit the keys:

            * Websites []

        :type json: array
        :returns JSON Response Object: JSON Response Object containing
            success or error response.
        """
        for key in SERVICEWEBSITEKEYS:
            if key not in json:
                return jsonify(Error='Missing credentials from submission: ' + key), 400

        handler = WebsiteHandler()
        sites = []
        siteIDs = []
        websiteInfo = []
        sites = (handler.unpackWebsites(json['websites']))
        dao = WebsiteDAO()

        if not sites:
            websiteInfo = None
        else:
            for x in sites:

                ID = (dao.removeWebsitesGivenServiceID(
                    sid=sid, wid=x['wid'], uid=uid))
                # print('Removed PhoneID '+str(x['phoneid']) + ' from service '+ str(sid))
                if(ID == None):
                    return jsonify(Error=
                        "Website ID not associated with Service-> sid: " + str(sid) + ' websiteid: ' + (str(x['wid']))),403
                else:
                    siteIDs.append(int(ID))
                    # print('Phones deleted IDs: '+ str(phoneIDs))
            for row in siteIDs:
                websiteInfo.append(_buildCoreWebsiteResponse(
                    website_tuple=dao.getWebsiteByID(row)))

        return jsonify({"websites":(websiteInfo)})

    def validateWebsites(self, list_of_websites):
        """
        Validate that a list of json websites consisting of keys "url" and
        "wdescription" are valid strings.

        :param list_of_websites: List of websites and descriptions
        :type list_of_websites: list
        :raises: ValueError, KeyError
        """
        if list_of_websites:
            checked_urls = []
            for site in list_of_websites:
                if not isinstance(site['url'], str) or site['url'].isspace() or site['url'] == "":
                    raise ValueError("Invalid url value: " + str(site['url']))
                if site['wdescription'] is not None:
                    if not isinstance(site['wdescription'], str) or site['wdescription'].isspace() or site['wdescription'] == "":
                        raise ValueError(
                            "Invalid wdescription value: " + str(site['wdescription']))

                if site['url'] not in checked_urls:
                    checked_urls.append(site['url'])
                else:
                    raise ValueError(
                        "Duplicate url's provided: " + str(site["url"]))
