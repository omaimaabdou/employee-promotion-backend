"""
The entry point to the backend of our premiere plugin
"""
from flask import Flask
import logging as log
from .config import MYSQL_PASSWORD,KEY_JWT,SQLALCHEMY_DATABASE_URI, MAIL_SERVER, MAIL_USERNAME, MAIL_PASSWORD
from flask_jwt_extended import JWTManager
from flask_restful import reqparse, Resource, Api, abort
from .models.models import *
from .resources.AuthResource import *
from .resources.EmployeeResource import *
from .resources.UserResource import *
log.basicConfig(format='%(levelname)s:%(message)s', level=log.DEBUG)
import datetime
def _create_app_and_api_objects():
    # load_model()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 1800    
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 50    
    app.config['SQLALCHEMY_POOL_SIZE'] = 10    
    app.config['JWT_SECRET_KEY'] = KEY_JWT
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
    app.config['MAIL_SERVER'] = MAIL_SERVER
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
    app.config['PROPAGATE_EXCEPTIONS'] = True
    jwt = JWTManager(app)
    db.init_app(app) #db defined in api_base
    api = Api(app)
    return app, api

def create_app():
    app, api = _create_app_and_api_objects()
    api.add_resource(AuthLoginResource, "/login")
    api.add_resource(AuthForgotPassword, "/forgot")
    api.add_resource(AuthResetPassword, "/reset")
    api.add_resource(AuthRegisterResource, "/register")
    api.add_resource(UserResource, "/user", "/user/<string:user_uid>")
    api.add_resource(EmployeeResource, "/employee", "/employee/<string:employee_uid>")

    return app
