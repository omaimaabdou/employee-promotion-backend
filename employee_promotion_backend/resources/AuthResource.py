import flask
from flask import Flask, request, jsonify, render_template
from flask import current_app

import os
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token, create_refresh_token,  get_current_user, get_jti, get_raw_jwt
import logging as log

from werkzeug.exceptions import InternalServerError
from flask_restful import reqparse, Resource, Api, abort
from ..models.models import *
from threading import Thread
import bcrypt
import datetime
import random
import string
from flask_mail import Mail, Message
import re
from functools import wraps
from flask_cors import cross_origin

# for validating an Email 
regex = "[^@]+@[^@]+\.[^@]{2,3}$"

app = Flask(__name__)



def send_async_email(app, msg):
    app.app_context().push()
    with app.app_context():
        try:
            mail = Mail(app)
            mail.send(msg)
        except ConnectionRefusedError:
            raise InternalServerError("[MAIL SERVER] not working")


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.recipients = recipients
    msg.body = text_body
    msg.html = html_body
    app = current_app._get_current_object()
    Thread(target=send_async_email, args=(app, msg)).start()


def checkLogin(newUser):
    username = newUser["username"]
    password = newUser["password"]
    user = User.query.filter_by(username=username).first()
    if user is None:
        return ""
    else:
        if (not (bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')))):
            return ""
        return user

class AuthLoginResource(Resource):
    @cross_origin()
    def post(self):
        if not request.is_json or request.content_length >= 50_000_000:
            return flask.make_response(flask.jsonify(success=False, error={"code": 100, "message": "Please send a valid json"}), 400)
        obj = request.get_json()
        resultUser = checkLogin(obj)
        if resultUser != "":
            delta = datetime.timedelta(days=1)
            access_token = create_access_token(identity=resultUser.uid, expires_delta=delta)
            userData = {
                'username': resultUser.username,
                'uid': resultUser.uid,
                'email': resultUser.email
            }
            return flask.make_response(flask.jsonify(success=True,
                                                     expiration_date=(datetime.datetime.now() + delta).strftime(
                                                         '%Y-%m-%dT%H:%M:%SZ'),
                                                     Token=access_token,
                                                     refresh_token=create_refresh_token(identity=resultUser.uid),
                                                     user=userData
                                                     ), 200)
        else:
            return flask.make_response(flask.jsonify(success=False, error={"code": 111, "message": "User not found"}), 404)

    @jwt_required
    @cross_origin()
    def delete(self):
        user_uid = get_jwt_identity()
        user = db.session.query(User).filter_by(uid=user_uid).first()
        user.refresh_token = None
        db.session.commit()
        return flask.jsonify(response="Successfully logged out", success=True)


class AuthRegisterResource(Resource):
    @cross_origin()
    def post(self):
        user = request.get_json()
        try:
            if not user["username"]:
                return flask.make_response(flask.jsonify(success=False, error={"code": 101, "message": "Please send username"}), 400)
            if not user["password"]:
                return flask.make_response(flask.jsonify(success=False, error={"code": 103, "message": "Please send password"}), 400)
            if not user["email"]:
                return flask.make_response(flask.jsonify(success=False, error={"code": 103, "message": "Please send email"}), 400)
            if not re.search(regex, user["email"]):
                return flask.make_response(flask.jsonify(success=False, error={"code": 103, "message": "Please send a valid email"}), 400)
        except KeyError:
            return flask.make_response(flask.jsonify(success=False, error={"code": 103, "message": "Please send username,password,email"}), 400)
    
        data_name = User.query.filter_by(username=user["username"]).first()
        data_email = User.query.filter_by(email=user["email"]).first()
        if data_name is None:
            if data_email is None:
                hashed = bcrypt.hashpw(user["password"].encode("utf-8"), bcrypt.gensalt())
                newUser = User(username=user["username"], password=hashed.decode("utf-8"), email=user["email"])
                db.session.add(newUser)
                db.session.flush()
                db.session.commit()
                return flask.make_response(flask.jsonify(resultat=user, success=True), 201)
            else:
                return flask.make_response(flask.jsonify(success=False, error={"code": 110, "message": "User email already exists"}), 409)
        else:
            return flask.make_response(flask.jsonify(success=False, error={"code": 110, "message": "User name already exists"}), 409)


class AuthForgotPassword(Resource):
    @cross_origin()
    def post(self):
        try:
            body = request.get_json()
            email = body.get('email')
            if not email:
                return flask.make_response(flask.jsonify(success=False, error={"code": 102, "message": "Please enter your email so you can reset your password."}), 400)

            user = User.query.filter_by(email=email).first()
            if not user:
                return flask.make_response(flask.jsonify(success=False, error={"code": 104, "message": "The provided email is not associated with an account."}), 400)

            token = ''.join(random.choice(string.octdigits + string.ascii_letters) for x in range(8))
            user.token = token
            db.session.commit()
            send_email('Reset your password',
                       sender='redaabdou49@gmail.com',
                       recipients=[user.email],
                       text_body=render_template('templates/reset_password.txt',
                                                 token=token),
                       html_body=render_template('templates/reset_password.html',
                                                 token=token))
            return flask.make_response(flask.jsonify(success=True), 200)
        except Exception as e:
            raise InternalServerError

    @cross_origin()
    def get(self):
        try:
            body = request.get_json()
            email = body.get('email')
            if not email:
                return flask.make_response(flask.jsonify(success=False, error={"code": 102, "message": "Please send email"}), 400)
            token = body.get('token')
            if not token:
                return flask.make_response(flask.jsonify(success=False, error={"code": 105, "message": "Please send token"}), 400)

            user = User.query.filter_by(email=email).first()
            if not user:
                return flask.make_response(flask.jsonify(success=False, error={"code": 104, "message": "Please send valid user"}), 400)

            token = user.token == body.get('token')
            return flask.jsonify(success=True)

        except Exception as e:
            raise InternalServerError


class AuthResetPassword(Resource):
    @cross_origin()
    def post(self):
        try:
            body = request.get_json()
            email = body.get('email')
            token = body.get('token')
            password = body.get('password')

            user = User.query.filter_by(email=email).first()

            if token != user.token:
                return flask.make_response(flask.jsonify(success=False, error={"code": 115, "message": "Token incorrect"}), 403)

            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            user.password = hashed.decode("utf-8")
            db.session.commit()
            send_email('Password Reset',
                       sender='redaabdou49@gmail.com',
                       recipients=[user.email],
                       text_body='Your password was succesfully reset.',
                       html_body='<p>Your password was succesfully reset.</p>')
            return flask.make_response(flask.jsonify(success=True), 200)
        except Exception as e:
            raise InternalServerError
