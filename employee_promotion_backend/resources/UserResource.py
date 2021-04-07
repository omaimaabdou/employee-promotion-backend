from flask import Flask, request
import os
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token, create_access_token
import logging as log
from flask_restful import reqparse, Resource, Api, abort
import flask
from models.models import *
import numpy as np

class UserResource(Resource):
    @jwt_required
    def get(self):
        user_uid = get_jwt_identity()
        result = db.session.query(User).filter_by(uid=user_uid).first()
        if result is not None:
            user = result.to_json()
            return flask.jsonify({"data": user, "success": True})
        else:
            return flask.make_response(flask.jsonify(success=False, error={"code": 100, "message": "error no user"}), 400)

    @jwt_required
    def put(self):
        if not request.is_json or request.content_length >= 50_000_000:
            return flask.make_response(flask.jsonify(success=False, error={"code": 100, "message": "Please send a valid json"}), 400)

        new_info = request.get_json()
        user_uid = get_jwt_identity()
        userDb = User.query.filter_by(uid=user_uid).first()
        userDb.update_user(user_uid, new_info)
        return flask.jsonify(success=True, code="", result="user_updated")

    @jwt_required
    def delete(self, user_uid: str):
        db.session.query(User).filter_by(uid=user_uid).delete()
        db.session.commit()

        return flask.jsonify(data=user_uid, success=True)
