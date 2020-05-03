from app import app
from flask import Flask, redirect, url_for, session, jsonify, request
from flask_login import current_user
from flask_dance.contrib.google import make_google_blueprint, google
from app.handlers.EventHandler import EventHandler
from app.handlers.RoomHandler import RoomHandler
from app.handlers.BuildingHandler import BuildingHandler
from app.handlers.ServiceHandler import ServiceHandler
from app.handlers.TagHandler import TagHandler
from app.handlers.PhoneHandler import PhoneHandler
from app.handlers.WebsiteHandler import WebsiteHandler
from app.oauth import admin_role_required, mod_role_required,user_role_required



@app.route("/API/App/Services/sid=<int:sid>", methods=['GET'])
@user_role_required
def getServiceByID(sid):
    """
    .. py:decorator:: user_role_required
    .. :quickref: Service; Get service by ID.

    Get Service By ID
    Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.getServiceByID`

    :param sid: Service ID
    :type sid: int
    :return: JSON

    **Example request**:

        .. sourcecode:: http

            GET /API/App/Services/sid=1 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
               
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 404: Service does not exist
    """
    if request.method == 'GET':
        return ServiceHandler().getServiceByID(sid=sid)
    else:
        return jsonify(Error="Method not allowed."), 405

###DASHBOARD ROUTES####
@app.route("/API/Dashboard/Services/offset=<int:offset>/limit=<int:limit>", methods=['GET'])
@mod_role_required
def getServicesSegmented(limit, offset):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Service; Get Services segmented

    Get Services segmented
    Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.getServicesSegmented`

    :param offset: Number of results to skip from top of list.
    :type offset: int
    :param limit: Number of results after offset to return.
    :type limit: int
    :return: JSON


    **Example request**:

        .. sourcecode:: http

            GET /API/App/Services/offset=0/limit=5 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
               
            }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    """
    if request.method == 'GET':
        return ServiceHandler().getServicesSegmented(limit=limit, offset=offset)
    else:
        return jsonify(Error="Method not allowed."), 405


@app.route("/API/Dashboard/Rooms/rid=<int:rid>/Services", methods=['GET'])
@mod_role_required
def getServicesByRoomID(rid):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Service; Get Services by given room ID.
    
    Get Service By Room ID
    Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.getServiceByRoomID`

    :return: JSON

    **Example request**:

      .. sourcecode:: http

          GET /API/Dashboard/Rooms/rid=<int:rid>/Services HTTP/1.1
          Host: inthenou.uprm.edu
          Accept: application/json
    
    **Request Body**:

      .. sourcecode:: json

            {
                
            }

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json


            {}
      :reqheader Cookie: Must contain session token to authenticate.
      :resheader Content-Type: application/json
      :statuscode 200: no error
      """
    if request.method == 'GET':
        return ServiceHandler().getServicesByRoomID(rid)
    else:
        return jsonify(Error="Method not allowed."), 405

# TODO: verify this is working with audit
@app.route("/API/Dashboard/Services/create", methods=['POST'])
@mod_role_required
def createService():
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Service; Create a service
    
    Create a Service
    Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.createService`

    :return: JSON

    **Example request**:

      .. sourcecode:: http

          GET /API/Dashboard/Services/create HTTP/1.1
          Host: inthenou.uprm.edu
          Accept: application/json
    
    **Request Body**:

      .. sourcecode:: json

            {
                
            }

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json


            {}
            
    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    """
    if request.method == 'POST':
        return ServiceHandler().createService(json=request.json,uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: ENSURE THE AUDIT CHANGE WORKS FOR THIS ROUTE.
@app.route("/API/Dashboard/Services/sid=<int:sid>/website/remove", methods=['POST'])
@mod_role_required
def removeServiceWebsite(sid):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Service; Remove Service Website
    
    Remove service website
    Uses :func:`~app.handlers.WebsiteHandler.WebsiteHandler.removeServiceWebsite`

    :return: JSON

    **Example request**:

      .. sourcecode:: http

          GET /API/Dashboard/Services/sid=1/website/remove HTTP/1.1
          Host: inthenou.uprm.edu
          Accept: application/json
    
    **Request Body**:

      .. sourcecode:: json

            {
                
            }

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {}
            
    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    """
    if request.method == 'POST':
        return WebsiteHandler().removeServiceWebsite(sid=sid, json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405

# TODO: ENSURE THE AUDIT CHANGE WORKS FOR THIS ROUTE.
@app.route("/API/Dashboard/Services/sid=<int:sid>/website/add", methods=['POST'])
@mod_role_required
def addServiceWebsite(sid):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Service; Add Service Website
    
    Insert service website
    Uses :func:`~app.handlers.WebsiteHandler.WebsiteHandler.insertServiceWebsite`

    :return: JSON

    **Example request**:

      .. sourcecode:: http

          GET /API/Dashboard/Services/sid=1/website/add" HTTP/1.1
          Host: inthenou.uprm.edu
          Accept: application/json
    
    **Request Body**:

      .. sourcecode:: json

            {
                
            }

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {}
            
    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    """
    if request.method == 'POST':
        return WebsiteHandler().insertServiceWebsite(sid=sid, json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: ENSURE THE AUDIT CHANGE WORKS FOR THIS ROUTE.
@app.route("/API/Dashboard/Services/sid=<int:sid>/phone/add", methods=['POST'])
@mod_role_required
def addServicePhone(sid):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Service; Add phone to service.
      
    Insert Service Phone
    Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.insertServicePhone`

    :return: JSON

    **Example request**:

    .. sourcecode:: http

      GET /API/Dashboard/Services/sid=1/phone/add HTTP/1.1
      Host: inthenou.uprm.edu
      Accept: application/json

    **Request Body**:

    .. sourcecode:: json

          {
                
          }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json


        {}
        
    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    """
    if request.method == 'POST':
        return PhoneHandler().insertServicePhone(sid=sid, uid=int(current_user.id), json=request.json)
    else:
        return jsonify(Error="Method not allowed."), 405

# TODO: ENSURE THE AUDIT CHANGE WORKS FOR THIS ROUTE.
@app.route("/API/Dashboard/Services/sid=<int:sid>/phone/remove", methods=['POST'])
@mod_role_required
def removeServicePhone(sid):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Service; Remove phone from service.
    
    Remove phone from service  
    Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.removePhoneByServiceID`

    :return: JSON

    **Example request**:

    .. sourcecode:: http

      GET /API/Dashboard/Services/sid=1/phone/remove HTTP/1.1
      Host: inthenou.uprm.edu
      Accept: application/json

    **Example response**:

      .. sourcecode:: http

          HTTP/1.1 200 OK
          Vary: Accept
          Content-Type: application/json


          {
             
          }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    """
    if request.method == 'POST':
        return PhoneHandler().removePhoneByServiceID(sid=sid, json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: check that this route is using audit properly
@app.route("/API/Dashboard/Services/sid=<int:sid>/update", methods=['POST'])
@mod_role_required
def updateService(sid):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Service; Update Service Informtion.
    
    Update Service Informtion  
    Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.updateServiceInformation`

    :return: JSON

    **Example request**:

    .. sourcecode:: http

      GET /API/Dashboard/Services/sid=1/update HTTP/1.1
      Host: inthenou.uprm.edu
      Accept: application/json
    
    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json


        {
               
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 404: Service does not exist
    """
    
    if request.method == 'POST':
        return ServiceHandler().updateServiceInformation(sid=sid, json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: check that this route is using audit properly
@app.route("/API/Dashboard/Services/sid=<int:sid>/delete", methods=['POST'])
@mod_role_required
def deleteService(sid):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Service; Delete Service with given ID.
    
    Delete Service 
    Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.deleteService`
    
    :return: JSON

    **Example request**:

    .. sourcecode:: http

      GET /API/Dashboard/Services/sid=1/delete HTTP/1.1
      Host: inthenou.uprm.edu
      Accept: application/json
    
    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json


        {
               
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 404: Service does not exist
    """
   
    if request.method == 'POST':
        return ServiceHandler().deleteService(sid=sid, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405


# TODO: check that this route is using audit properly
@app.route("/API/Dashboard/Rooms/rid=<int:rid>/changeCoordinates", methods=['POST'])
@mod_role_required
def changeRoomCoordinates(rid):
    """
    .. py:decorator:: mod_role_required
    .. :quickref: Room; Change room coordinates.
    
    Change Room coordinates   
    Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.changeRoomCoordinates`

    :return: JSON

    **Example request**:

    .. sourcecode:: http

      GET /API/Dashboard/Rooms/rid=1/changeCoordinates HTTP/1.1
      Host: inthenou.uprm.edu
      Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json


        {
               
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    :statuscode 404: Service does not exist
    """
    if request.method == 'POST':
        return RoomHandler().changeRoomCoordinates(rid=rid, json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405
