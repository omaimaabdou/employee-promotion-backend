from flask import Flask, request
import os
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token, create_access_token
import logging as log
from flask_restful import reqparse, Resource, Api, abort
import flask
from ..models.models import *
import numpy as np

class EmployeeResource(Resource):
    @jwt_required
    def get(self, employee_uid):
        result = db.session.query(Employee).filter_by(uid=employee_uid).first()
        employee = result.to_json()
        return flask.jsonify(data=employee, success=True)
    
    @jwt_required
    def post(self):
        if not request.is_json or request.content_length >= 50_000_000:
            return flask.make_response(flask.jsonify(success=False, error={"code": 100, "message": "Please send a valid json"}), 400)
        obj = request.get_json()
        try : 
            employee = Employee(email=obj.get("email"),
                                first_name=obj.get("first_name"),
                                last_name=obj.get("last_name"),
                                situation_sociale=obj.get("situation_sociale"),
                                age=obj.get("age"),
                                degree=obj.get("degree"),
                                grade=obj.get("grade"),
                                grade_seniority=obj.get("grade_seniority"))
        except :
            return flask.jsonify(message="Please send all informations", success=False)
        return flask.jsonify(data=employee.to_json(), success=True)

    @jwt_required
    def put(self, employee_uid):
        if not request.is_json or request.content_length >= 50_000_000:
            return flask.make_response(flask.jsonify(success=False, error={"code": 100, "message": "Please send a valid json"}), 400)

        obj = request.get_json()
        obj["updated_at"]=db.func.now()
        db.session.query(Employee).filter_by(uid=employee_uid).update(obj)
        db.session.commit()

        return flask.jsonify(data=employee_uid, success=True, message="employee_updated")

    @jwt_required
    def delete(self, employee_uid: str):
        db.session.query(Employee).filter_by(uid=employee_uid).delete()
        db.session.commit()

        return flask.jsonify(data=employee_uid, success=True, message="employee_deleted")