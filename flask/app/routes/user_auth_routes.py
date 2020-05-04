from app import app
from flask import Flask, g, flash, redirect, url_for, render_template, session, request, jsonify
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer.requests import OAuth1Session
from flask_dance.consumer import oauth_before_login
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask import Flask, redirect, url_for, flash, render_template, session, make_response
from flask_login import login_required, logout_user, current_user
from app.models import db, User, OAuth
from app.handlers.TagHandler import TagHandler
from app.oauth import *
from app.config import *
from sqlalchemy.orm.exc import NoResultFound
from dotenv import load_dotenv
load_dotenv()

SIGNUPKEYS = ['id', 'display_name', 'access_token', 'email', 'tags']

# route used to logout user, must be logged in to access
@app.route("/API/App/logout")
@user_role_required
def app_logout():
    """
    .. py:decorator:: user_role_required
    .. :quickref: OAuth; Logout
    
    Logout
    Uses :func:`~app.models.OAuth.filter_by`

    
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        GET /API/App/logout HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json

    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
            "Error": "You have loged out "
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 200: no error
    :statuscode 403: User is not logged in.
    """
    query = OAuth.query.filter_by(token=str(session['token']))
    try:
        oauth = query.one()
        db.session.delete(oauth)
        db.session.commit()
    except NoResultFound:
        return jsonify(Error="You need a session in the system, try loggin in  "),403
    logout_user()
    
    return jsonify(Error="You have loged out "),200

@app.route("/API/App/signup", methods=['POST'])
def signup():
    """
    .. :quickref: OAuth; Singup
    
    Signup
    Uses :func:`~app.TagHandler.TagHandler.batchSetUserTags` as well as
        :func:`~app.UserHandler.UserHandler.getUserByID`

    
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        GET /API/App/signup HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json
    
    **Body of Request**:

        .. code-block:: json

            {

                "access_token":"test_Token",
                "id":"113768707919850641968",
                "email":"jonathan.santiago27@upr.edu",
                "display_name":"Jonathan X Santiago Gonzalez",
                "tags":[	{"tid":1,"tname":"ADMI","tagweight":0},
            			    {"tid":2,"tname":"ADOF","tagweight":0},
            			    {"tid":3,"tname":"AGRO","tagweight":0},
            			    {"tid":4,"tname":"ALEM","tagweight":0},
            			    {"tid":5,"tname":"ANTR","tagweight":0}]	

            }
                
    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 403 FORBIDDEN
        Vary: Accept
        Content-Type: text/javascript

        {
            "Error": "User with that email exists <User 11>"
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: User Created
    :statuscode 403: User with that email exists
    """
    if request.method == 'POST':
        
        if not request.json:
            return jsonify(Error="No JSON provided."), 400
        info = request.json
        local={}
        for key in info:
            if key in SIGNUPKEYS:
                local[key]=info[key]
        
        for key in SIGNUPKEYS:
            if key not in local:
                return jsonify(Error="Missing input parameter: "+str(key))
            
        user_usub = local["id"]
        query = User.query.filter_by(provider=user_usub)
        
        try:
            user = query.one()
            return jsonify(Error="User with that email exists "+str(user)),403
        except NoResultFound:
        # Create account for new user
            print("User being created")
            user = User(email=local["email"],
                    provider=user_usub,
                    display_name=local["display_name"],
                    user_type="Student",
                    user_role=int(1),
                    role_issuer=int(1),
                    )
            if(user):
                db.session.add_all([user])
                db.session.commit()
            
            query = OAuth.query.filter_by(
                    token= local['access_token'], id=user.id, user=user)
            
            try:
                oauth = query.one()
            except NoResultFound:
                oauth = OAuth(token=local['access_token'], id=user.id, user=user, created_at="5223213.12",provider="google")
                db.session.add_all([oauth])
                db.session.commit()
                login_user(oauth.user)
                info['uid']=int(current_user.id)
                print("Registering tags : "+str(local["tags"]))
                
                tags =   TagHandler().batchSetUserTags(uid= user.id,json=info, weight=100, no_json=True)
                tags['User'] = UserHandler().getUserByID(current_user.id,no_json=True)
            return (tags), 201
    else:
        return jsonify(Error="Method not allowed."), 405

@app.route("/API/App/login", methods=['POST'])
def app_login():
    """
    .. :quickref: OAuth; Login
    
    Login
    
    
    :return: JSON

    **Example request**:

    .. sourcecode:: http

        GET /API/App/login HTTP/1.1
        Host: inthenou.uprm.edu
        Accept: application/json
    
    **Body of Request**:

        .. code-block:: json

            {
                "access_token":"test_Token",
                "id":"113768707919850641968",
                "email":"jonathan.santiago27@upr.edu",
                "display_name":"Jonathan X Santiago Gonzalez"
            }
            
    **Example response**:

    .. sourcecode:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
            "uid": "11"
        }

    :reqheader Cookie: Must contain session token to authenticate.
    :resheader Content-Type: application/json
    :statuscode 201: User Created
    :statuscode 403: User with that email exists
    """
    info = request.json
    user_usub = info["id"]
    query = User.query.filter_by(provider=user_usub)
    try:
        user = query.one()
        
    except NoResultFound:
        token = {"Token":"This_is_a_token"}
        return jsonify(token),200

    query = OAuth.query.filter_by(
        token = info['access_token'], id=user.id, user=user)
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(token=info['access_token'], id=user.id, user=user, created_at="5223213.12",provider="google")
        db.session.add_all([oauth])
        db.session.commit()
    login_user(oauth.user)
    session['token']=info['access_token']
    flash("Successfully signed in.")
    # sessionDict = str(session)[20:-1]
    # # print(sessionDict)
    # # {'_fresh': True, '_id': '934028cbba09af9ef6c35734f503a02c84a5f9d54e92c85bd1b3c7b0eb9167791a93fe9cf0a6a57c1af31d4d319031a244a2514124fa970b7ebb39d06249737f', '_user_id': '2', 'token': 'ya29.a0Ae4lvC25jHQPYb40hlyWPdxeVpgE8lPKEhYURwbfNkWdfO-4z4joM3zZByq1UlFdXbjt5y40-qYGy3lClOL6ffCyWRIYIBfgbia-vKBpA5Aspd5LNNIueAJI-zlO04k-vPHYUxmP2r3imNF33avaI3Xe0-3jSS-yOrNV"}
    # cookie = encodeFlaskCookie(secret_key=os.getenv(
    #     "FLASK_SECRET_KEY"), cookieDict=sessionDict)
    # # print(cookie)
    # session['cookys'] = cookie
    # # print(decodeFlaskCookie(secret_key=os.getenv("FLASK_SECRET_KEY"), cookieValue=cookie))

    response = make_response({"uid": str(user.id)})
    
    response.headers['Session']=str(session)

    return (response)



################## DASHBOARD ROUTES ######################

# @oauth_before_login.connect
# def before_google_login(blueprint, url):
#     try:
#         Usersession = request.headers['session']
#         print("session Cached")
#     except:
#         print("redirecting to google")


# @app.route("/API/login", methods=['GET'])
# @login_required
# def dashboard_login():
#     try:
#         (current_user.id)
#         return UserHandler().getUserByID(int(current_user.id))
#     except:
#         session['AppLogin'] = False
#         # query = User.query.filter_by(email="kensy.bernadeau@upr.edu")
#         # user = query.one()
#         # print('Session Defined as ' + str(session['AppLogin']))
#         # login_user(user)
#         # #flash ("No user found ")
        
#         return redirect(url_for(("google.login")))
        


# @app.route("/API/logout")
# @login_required
# def dashboard_logout():
#     query = OAuth.query.filter_by(token=str(session['token']))
#     try:
#         oauth = query.one()
#         db.session.delete(oauth)
#         db.session.commit()
#     except NoResultFound:
#         print("NO RESULT FOUND ")
#     logout_user()
#     flash("You have logged out")
#     return render_template("dashhome.html")


# @app.route("/API/home")
# #@login_required
# def dashboard_home():
#     return render_template("html/index.html")
