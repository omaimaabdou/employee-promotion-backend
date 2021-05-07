from flask import Flask, request
import os
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token, create_access_token
import logging as log
from flask_restful import reqparse, Resource, Api, abort
import flask
from ..models.models import *
import numpy as np
from sqlalchemy import asc, desc 
from sqlalchemy.sql import text

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
                                social_situation=obj.get("social_situation"),
                                age=obj.get("age"),
                                degree=obj.get("degree"),
                                grade=obj.get("grade"),
                                grade_seniority=obj.get("grade_seniority"))
        except :
            return flask.jsonify(message="Please send all informations", success=False)
        
        db.session.add(employee)
        db.session.flush()
        db.session.commit()
        return flask.jsonify(data=employee.to_json(), success=True)

    @jwt_required
    def put(self, employee_uid):
        if not request.is_json or request.content_length >= 50_000_000:
            return flask.make_response(flask.jsonify(success=False, error={"code": 100, "message": "Please send a valid json"}), 400)

        obj = request.get_json()
        db.session.query(Employee).filter_by(uid=employee_uid).update(obj)
        db.session.commit()

        return flask.jsonify(data=employee_uid, success=True, message="employee_updated")

    @jwt_required
    def delete(self, employee_uid: str):
        db.session.query(Employee).filter_by(uid=employee_uid).delete()
        db.session.commit()

        return flask.jsonify(data=employee_uid, success=True, message="employee_deleted")

class EmployeesResource(Resource):
    @jwt_required
    def post(self):
        if not request.is_json or request.content_length >= 50_000_000:
            return flask.make_response(flask.jsonify(success=False, error={"code": 100, "message": "Please send a valid json"}), 400)
        obj = request.get_json()

        per_page=20

        if obj.get("page"):
            page = obj.get("page")
        else:
            page = 1

        if obj.get("keyword"):
            employees = db.session.query(Employee).filter(Employee.last_name.ilike('%{0}%'.format(obj.get("keyword")))).order_by(text("created_at desc")).paginate(page, per_page, False)
            total = employees.total
            record_items = employees.items

        else:
            employees = db.session.query(Employee).order_by(text("created_at desc")).paginate(page, per_page, False)
            total = employees.total
            record_items = employees.items
        
        get_employees=[]

        for employee in record_items :
            employee_dict = {}

            employee_dict["uid"] = employee.uid
            employee_dict["email"] = employee.email
            employee_dict["first_name"] = employee.first_name
            employee_dict["last_name"] = employee.last_name
            employee_dict["social_situation"] = employee.social_situation
            employee_dict["entry_date"] = employee.entry_date
            employee_dict["age"] = employee.age
            employee_dict["degree"] = employee.degree
            employee_dict["grade"] = employee.grade
            employee_dict["grade_seniority"] = employee.grade_seniority
            employee_dict["created_at"] = employee.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            employee_dict["updated_at"] = employee.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

            get_employees.append(employee_dict)

        return flask.jsonify(data=get_employees, count=total, success=True)


