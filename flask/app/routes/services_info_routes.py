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
            "numbers": null,
            "websites": null,
            "isdeleted": false,
            "room": {
                "building": {
                    "babbrev": "S",
                    "bcommonname": "STEFANI",
                    "bid": 1,
                    "bname": "LUIS A STEFANI (INGENIERIA)",
                    "btype": "Académico",
                    "distinctfloors": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7
                ],
                    "numfloors": 7,
                    "photourl": null
                },
                "photourl": null,
                "raltitude": 50.04,
                "rcode": "123A1",
                "rcustodian": "naydag.santiago@upr.edu",
                "rdept": "INGENIERIA ELECTRICA",
                "rdescription": "CAPSTONE",
                "rfloor": 1,
                "rid": 56,
                "rlatitude": 50.04,
                "rlongitude": 50.04,
                "roccupancy": 0
            },
            "sdescription": "Capstone TA Office Hours; Available to answer questions.",
            "sid": 1,
            "sname": "Office Hours: Victor Lugo",
            "sschedule": "L, W: 9:30am - 10:30am"
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

            GET /API/App/Services/offset=0/limit=3 HTTP/1.1
            Host: inthenou.uprm.edu
            Accept: application/json

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                           "services": [
                    {
                        "numbers": null,
                        "room": {
                            "building": {
                                "babbrev": "S",
                                "bcommonname": "STEFANI",
                                "bid": 1,
                                "bname": "LUIS A STEFANI (INGENIERIA)",
                                "btype": "Académico",
                                "distinctfloors": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7
                                ],
                                "numfloors": 7,
                                "photourl": null
                            },
                            "photourl": null,
                            "raltitude": 50.04,
                            "rcode": "123A1",
                            "rcustodian": "naydag.santiago@upr.edu",
                            "rdept": "INGENIERIA ELECTRICA",
                            "rdescription": "CAPSTONE",
                            "rfloor": 1,
                            "rid": 56,
                            "rlatitude": 50.04,
                            "rlongitude": 50.04,
                            "roccupancy": 0
                        },
                        "sdescription": "Capstone TA Office Hours; Available to answer questions.",
                        "sid": 2,
                        "sname": "Office Hours: David Riquelme",
                        "sschedule": "M, V: 2:30pm - 3:30pm",
                        "websites": null
                    },
                    {
                        "numbers": [
                            {
                                "phoneid": 3,
                                "pnumber": "787-832-4040,5842",
                                "ptype": "E"
                            }
                        ],
                        "room": {
                            "building": {
                                "babbrev": "S",
                                "bcommonname": "STEFANI",
                                "bid": 1,
                                "bname": "LUIS A STEFANI (INGENIERIA)",
                                "btype": "Académico",
                                "distinctfloors": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7
                                ],
                                "numfloors": 7,
                                "photourl": null
                            },
                            "photourl": null,
                            "raltitude": 50.04,
                            "rcode": "229A",
                            "rcustodian": "jfernando.vega@upr.edu",
                            "rdept": "INGENIERIA ELECTRICA",
                            "rdescription": "OFICINA PROFESOR DR. FERNANDO VEGA ",
                            "rfloor": 2,
                            "rid": 151,
                            "rlatitude": 50.04,
                            "rlongitude": 50.04,
                            "roccupancy": 0
                        },
                        "sdescription": "Office Hours to discuss class topics, and consult with Capstone Team.",
                        "sid": 3,
                        "sname": "Office Hours: Fernando Vega",
                        "sschedule": "L: 3:30pm - 4:30pm, W: 1:30pm - 3:30pm",
                        "websites": [
                            {
                                "url": "http://ece.uprm.edu/~fvega/",
                                "wdescription": "J. Fernando Vega-Riveros, Ph.D. Professor",
                                "wid": 2
                            }
                        ]
                    },
                    {
                        "numbers": [
                            {
                                "phoneid": 1,
                                "pnumber": "787-832-4040,3182",
                                "ptype": "E"
                            },
                            {
                                "phoneid": 2,
                                "pnumber": "(787) 831-7564",
                                "ptype": "F"
                            }
                        ],
                        "room": {
                            "building": {
                                "babbrev": "S",
                                "bcommonname": "STEFANI",
                                "bid": 1,
                                "bname": "LUIS A STEFANI (INGENIERIA)",
                                "btype": "Académico",
                                "distinctfloors": [
                                    1,
                                    2,
                                    3,
                                    4,
                                    5,
                                    6,
                                    7
                                ],
                                "numfloors": 7,
                                "photourl": null
                            },
                            "photourl": null,
                            "raltitude": 50.04,
                            "rcode": "224",
                            "rcustodian": "jose.colom1@upr.edu",
                            "rdept": "INGENIERIA ELECTRICA",
                            "rdescription": "OFICINA MRS. VERONICA VAZQUEZ / MRS. MARITZA FIGUEROA",
                            "rfloor": 2,
                            "rid": 134,
                            "rlatitude": 50.04,
                            "rlongitude": 50.04,
                            "roccupancy": 0
                        },
                        "sdescription": "Counseling and guidance for students with regards to their academic carreers and progress.",
                        "sid": 4,
                        "sname": "ECE Counseling",
                        "sschedule": "L-V: 7:30am-12:30pm, 1:30pm-4:30pm",
                        "websites": [
                            {
                                "url": "https://ece.uprm.edu/student-services/conseling/",
                                "wdescription": "Counselors",
                                "wid": 1
                            }
                        ]
                    }
                ]
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
    
    **Example response**:

      .. sourcecode:: json

            {
                "services": 
                [
                    {
                        "numbers": 
                        [
                            {
                                "phoneid": 6,
                                "pnumber": "973-225-7484",
                                "ptype": "M"
                            },
                            {
                                "phoneid": 7,
                                "pnumber": "803-233-6617",
                                "ptype": "M"
                            },
                            {
                                "phoneid": 4,
                                "pnumber": "{{phone_numberService}}",
                                "ptype": "{"
                            },
                            {
                                "phoneid": 5,
                                "pnumber": "{{phone_numberService2}}",
                                "ptype": "{"
                            }
                        ],
                        "websites": 
                        [
                            {
                                "url": "http://dandre.net",
                                "wdescription": "{{wdescriptionService}}",
                                "wid": 3
                            },
                            {
                                "url": "http://lorempixel.com/640/480/city",
                                "wdescription": "{{wdescriptionService2}}",
                                "wid": 4
                            }
                        ],
                        "sdescription": "bleeding-edge target synergies",
                        "sid": 5,
                        "sname": "navigating",
                        "sschedule": "Sat Nov 07 2020 09:20:48 GMT-0400 (AST)"
                    },
                    {
                        "numbers": 
                        [
                            {
                                "phoneid": 10,
                                "pnumber": "988-156-1109",
                                "ptype": "M"
                            },
                            {
                                "phoneid": 11,
                                "pnumber": "967-166-6979",
                                "ptype": "M"
                            },
                            {
                                "phoneid": 4,
                                "pnumber": "{{phone_numberService}}",
                                "ptype": "{"
                            },
                            {
                                "phoneid": 5,
                                "pnumber": "{{phone_numberService2}}",
                                "ptype": "{"
                            }
                        ],
                        "websites": 
                        [
                            {
                                "url": "https://maudie.info",
                                "wdescription": "{{wdescriptionService}}",
                                "wid": 5
                            },
                            {
                                "url": "http://lorempixel.com/640/480/city",
                                "wdescription": "{{wdescriptionService2}}",
                                "wid": 4
                            },
                            {
                                "url": "http://noemy.org",
                                "wdescription": "",
                                "wid": 7
                            },
                            {
                                "url": "https://wanda.biz",
                                "wdescription": "Non maxime est nesciunt suscipit qui ea omnis qui.",
                                "wid": 8
                            }
                        ],
                        "sdescription": "bleeding-edge generate partnerships",
                        "sid": 6,
                        "sname": "connecting",
                        "sschedule": "Fri Jul 31 2020 16:09:45 GMT-0400 (AST)"
                    },
                    {
                        "numbers": 
                        [
                            {
                                "phoneid": 14,
                                "pnumber": "831-000-5089",
                                "ptype": "M"
                            },
                            {
                                "phoneid": 15,
                                "pnumber": "267-476-7589",
                                "ptype": "M"
                            },
                            {
                                "phoneid": 4,
                                "pnumber": "{{phone_numberService}}",
                                "ptype": "{"
                            },
                            {
                                "phoneid": 5,
                                "pnumber": "{{phone_numberService2}}",
                                "ptype": "{"
                            }
                        ],
                        "websites": 
                        [
                            {
                                "url": "https://jarred.com",
                                "wdescription": "{{wdescriptionService}}",
                                "wid": 9
                            },
                            {
                                "url": "http://lorempixel.com/640/480/city",
                                "wdescription": "{{wdescriptionService2}}",
                                "wid": 4
                            },
                            {
                                "url": "https://destiney.name",
                                "wdescription": "",
                                "wid": 11
                            },
                            {
                                "url": "https://hildegard.biz",
                                "wdescription": "Voluptatum esse laboriosam velit repudiandae sed voluptates ratione laboriosam molestiae.",
                                "wid": 12
                            },
                            {
                                "url": "https://lester.org",
                                "wdescription": "",
                                "wid": 13
                            },
                            {
                                "url": "https://myrtle.com",
                                "wdescription": "Impedit sit sint aut molestias iusto.",
                                "wid": 14
                            }
                        ],
                        "sdescription": "New service description",
                        "sid": 7,
                        "sname": "new Service Name",
                        "sschedule": "New service schedule"
                    }
                ]
            }

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

            "uid":"{{uidService}}",
            "rid":"{{ridService}}",
            "sname":"{{$randomIngverb}}",
            "sdescription":"{{$randomBs}}",
            "sschedule":"{{$randomDateFuture}}",
            "numbers":[		
            			{"pnumber":"{{phone_numberService}}","ptype":"{{ptypeService}}"	},	
            			{"pnumber":"{{phone_numberService2}}","ptype":"{{ptypeService2}}"}
            		   ],
            "websites":[		
            			{"url":"{{websiteService}}","wdescription":"{{wdescriptionService}}"},	
            			{"url":"{{websiteService2}}","wdescription":"{{wdescriptionService2}}"}	

            			]				

            }

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json
            
            {
                "numbers": 
                [
                    {
                        "phoneid": 4,
                        "pnumber": "{{phone_numberService}}",
                        "ptype": "m"
                    },
                    {
                        "phoneid": 5,
                        "pnumber": "{{phone_numberService2}}",
                        "ptype": "m"
                    }
                ],
                "websites": 
                [
                    {
                        "url": "https://jarred.com",
                        "wdescription": "{{wdescriptionService}}",
                        "wid": 9
                    },
                    {
                        "url": "http://lorempixel.com/640/480/city",
                        "wdescription": "{{wdescriptionService2}}",
                        "wid": 4
                    }
                ],
                "isdeleted": false,
                "room": {
                    "building": {
                        "babbrev": "S",
                        "bcommonname": "STEFANI",
                        "bid": 1,
                        "bname": "LUIS A STEFANI (INGENIERIA)",
                        "btype": "Académico",
                        "distinctfloors": [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7
                        ],
                        "numfloors": 7,
                        "photourl": null
                    },
                    "photourl": null,
                    "raltitude": 50.04,
                    "rcode": "100",
                    "rcustodian": "pedro.rivera25@upr.edu",
                    "rdept": "INGENIERIA ELECTRICA",
                    "rdescription": "COBACHA CONSERJE",
                    "rfloor": 1,
                    "rid": 1,
                    "rlatitude": 50.04,
                    "rlongitude": 50.04,
                    "roccupancy": 0
                },
                "sdescription": "rich transform infrastructures",
                "sid": 7,
                "sname": "bypassing",
                "sschedule": "Tue Sep 29 2020 19:38:03 GMT-0400 (AST)"
            }
            
    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: CREATED
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
                "websites":	

                [	
            	    {"wid":"{{wid}}"}, 
            	    {"wid":"{{wid2}}"} 		
                ]	

            }

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept
            Content-Type: application/json


            {
                "websites": 
                [
                    {
                        "url": "https://jose.org",
                        "wid": 32
                    },
                    {
                        "url": "http://sally.biz",
                        "wid": 31
                    }
                ]
            }
            
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
	
                "websites":
                [	
                
                    {"url":"{{website}}","wdescription":"{{wdescription}}"},	
                    {"url":"{{website2}}","wdescription":"{{wdescription2}}"}

                ]				

            }

    **Example response**:

        .. sourcecode:: http

            HTTP/1.1 201 CREATED
            Vary: Accept
            Content-Type: application/json


            {
                "websites": 
                [
                    {
                        "url": "http://sally.biz",
                        "wdescription": "",
                        "wid": 31
                    },
                    {
                        "url": "https://jose.org",
                        "wdescription": "Aut minima incidunt cupiditate aut excepturi est est dolorem.",
                        "wid": 32
                    }
                ]
            }
            
    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: created
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
            	"numbers":	
            	[	
             
            	{"pnumber":"{{phone_number}}","ptype":"{{ptype}}"},	
            	{"pnumber":"{{phone_number2}}","ptype":"{{ptype2}}"}		

            	]	

            }

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 201 CREATED
        Vary: Accept
        Content-Type: application/json


        {
            "numbers":
            [
                {
                    "pnumber": "831-000-5089",
                    "ptype": "m"
                },
                {
                    "pnumber": "267-476-7589",
                    "ptype": "m"
                }
            ]
        }
        
    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    """
    if request.method == 'POST':
        return PhoneHandler().insertServicePhone(sid=sid, uid=int(current_user.id), json=request.json) , 201
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
     
    **Request Body**:

    .. sourcecode:: json

            {
            	"numbers":	
                [	
            	{"phoneid":"{{pid}}"}, 
            	{"phoneid":"{{pid2}}"} 		
                ]	

            }
    **Example response**:

      .. sourcecode:: http

          HTTP/1.1 200 OK
          Vary: Accept
          Content-Type: application/json


            {
                "numbers": 
                [
                    {
                        "pnumber": "667-882-6107",
                        "ptype": "m"
                    },
                    {
                        "pnumber": "338-042-3699",
                        "ptype": "m"
                    }
                ]
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
    
    **Request Body**:

    .. sourcecode:: json

            {
                "sname":"new Service Name", 
                "sdescription":"New service description", 
                "sschedule":"New service schedule", 
                "rid":{{rid}}	
            }
    
    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json


            {
                "numbers": 
                [
                    {
                        "phoneid": 97,
                        "pnumber": "723-186-6255",
                        "ptype": "M"
                    },
                    {
                        "phoneid": 98,
                        "pnumber": "929-005-8183",
                        "ptype": "M"
                    }
                ],
                "room": {
                    "building": {
                        "babbrev": "S",
                        "bcommonname": "STEFANI",
                        "bid": 1,
                        "bname": "LUIS A STEFANI (INGENIERIA)",
                        "btype": "Académico",
                        "distinctfloors": [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7
                        ],
                        "numfloors": 7,
                        "photourl": null
                    },
                    "photourl": null,
                    "raltitude": 149.9028,
                    "rcode": "100",
                    "rcustodian": "pedro.rivera25@upr.edu",
                    "rdept": "INGENIERIA ELECTRICA",
                    "rdescription": "COBACHA CONSERJE",
                    "rfloor": 1,
                    "rid": 1,
                    "rlatitude": -81.2338,
                    "rlongitude": 177.3793,
                    "roccupancy": 0
                },
                "sdescription": "New service description",
                "sid": 1,
                "sname": "new Service Name ",
                "sschedule": "New service schedule",
                "websites": [
                    {
                        "url": "http://talia.org",
                        "wdescription": "",
                        "wid": 51
                    },
                    {
                        "url": "https://otilia.org",
                        "wdescription": "Quibusdam impedit rem nesciunt soluta.",
                        "wid": 52
                    }
                ]
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
            "numbers": [
                {
                    "phoneid": 97,
                    "pnumber": "723-186-6255",
                    "ptype": "M"
                },
                {
                    "phoneid": 98,
                    "pnumber": "929-005-8183",
                    "ptype": "M"
                }
            ],
            "room": {
                "building": {
                    "babbrev": "S",
                    "bcommonname": "STEFANI",
                    "bid": 1,
                    "bname": "LUIS A STEFANI (INGENIERIA)",
                    "btype": "Académico",
                    "distinctfloors": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7
                    ],
                    "numfloors": 7,
                    "photourl": null
                },
                "photourl": null,
                "raltitude": 149.9028,
                "rcode": "100",
                "rcustodian": "pedro.rivera25@upr.edu",
                "rdept": "INGENIERIA ELECTRICA",
                "rdescription": "COBACHA CONSERJE",
                "rfloor": 1,
                "rid": 1,
                "rlatitude": -81.2338,
                "rlongitude": 177.3793,
                "roccupancy": 0
            },
            "sdescription": "New service description",
            "sid": 1,
            "sname": "new Service Name ",
            "sschedule": "New service schedule",
            "websites": [
                {
                    "url": "http://talia.org",
                    "wdescription": "",
                    "wid": 51
                },
                {
                    "url": "https://otilia.org",
                    "wdescription": "Quibusdam impedit rem nesciunt soluta.",
                    "wid": 52
                }
            ]
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
    
    **Request Body**:

    .. sourcecode:: json

            {
            	"rlatitude":"{{$randomLatitude}}",
            	"rlongitude":"{{$randomLongitude}}",
            	"raltitude":"{{$randomLongitude}}"

            }
            
    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json


        {
            "raltitude": 1.1006,
            "rcode": "100",
            "rfloor": 1,
            "rid": 1,
            "rlatitude": 56.7699,
            "rlongitude": 9.1135
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
