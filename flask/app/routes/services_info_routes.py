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
      
      Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.getServiceByID`

      Get Service By ID
      
      .. :quickref: Service; Get Service By ID.

      :return: JSON

      **Example request**:

      .. sourcecode:: http

        GET /API/App/Services/sid=<int:sid> HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

      :reqheader Cookie: Must contain session token to authenticate.
      :resheader Content-Type: application/json
      :statuscode 200: no error
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
      
      Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.getServiceSegmented`

      Get Service By ID
      
      .. :quickref: Service; Get Services segmented.

      :return: JSON

      **Example request**:

      .. sourcecode:: http

        GET /API/Dashboard/Services/offset=<int:offset>/limit=<int:limit> HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

      :reqheader Cookie: Must contain session token to authenticate.
      :resheader Content-Type: application/json
      :statuscode 200: no error
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
      
      Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.getServiceByRoomID`

      Get Service By Room ID
      
      .. :quickref: Service; Get Services by given room ID.

      :return: JSON

      **Example request**:

      .. sourcecode:: http

        GET /API/Dashboard/Rooms/rid=<int:rid>/Services HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

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
      
      Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.createService`

      Create Service
      
      .. :quickref: Service; Create a service

      :return: JSON

      **Example request**:

      .. sourcecode:: http

        GET /API/Dashboard/Services/create HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

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
      
      Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.removeServiceWebsite`

      Remove service websites 
      
      .. :quickref: Service; Remove service website

      :return: JSON

      **Example request**:

      .. sourcecode:: http

        GET /API/Dashboard/Services/sid=<int:sid>/website/remove HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

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
      
      Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.addServiceWebsite`

      Add Service Website
      
      .. :quickref: Service; Add service Website                                                     

      :return: JSON

      **Example request**:

      .. sourcecode:: http

        GET /API/Dashboard/Services/sid=<int:sid>/website/add HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

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
      
      Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.insertServicePhone`

      Insert Service Phone
      
      .. :quickref: Service; Add phone to service.

      :return: JSON

      **Example request**:

      .. sourcecode:: http

        GET /API/Dashboard/Services/sid=<int:sid>/phone/add HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

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
      
      Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.removePhoneByServiceID`

      Remove phone from service
      
      .. :quickref: Service; Remove phone from service.

      :return: JSON

      **Example request**:

      .. sourcecode:: http

        GET /API/Dashboard/Services/sid=<int:sid>/phone/remove HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

      :reqheader Cookie: Must contain session token to authenticate.
      :resheader Content-Type: application/json
      :statuscode 200: no error
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
      
      Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.updateServiceInformation`

      Update Service Informtion
      
      .. :quickref: Service; Update Service Informtion.

      :return: JSON

      **Example request**:

      .. sourcecode:: http

        GET /API/Dashboard/Services/sid=<int:sid>/update HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

      :reqheader Cookie: Must contain session token to authenticate.
      :resheader Content-Type: application/json
      :statuscode 200: no error
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
      
      Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.deleteService`

     Delete Service 
      
      .. :quickref: Service; Delete Service with given ID.

      :return: JSON

      **Example request**:

      .. sourcecode:: http

        GET /API/Dashboard/Services/sid=<int:sid>/delete HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

      :reqheader Cookie: Must contain session token to authenticate.
      :resheader Content-Type: application/json
      :statuscode 200: no error
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
      
      Uses :func:`~app.handlers.ServiceHandler.ServiceHandler.changeRoomCoordinates`

      Change Room coordinates 
      
      .. :quickref: Room; Change room coordinates.

      :return: JSON

      **Example request**:

      .. sourcecode:: http

        GET /API/Dashboard/Rooms/rid=<int:rid>/changeCoordinates HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

      :reqheader Cookie: Must contain session token to authenticate.
      :resheader Content-Type: application/json
      :statuscode 200: no error
      """
    if request.method == 'POST':
        return RoomHandler().changeRoomCoordinates(rid=rid, json=request.json, uid=int(current_user.id))
    else:
        return jsonify(Error="Method not allowed."), 405
