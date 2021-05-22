from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass, field
from typing import List, Union, TypeVar, Type, Optional
from uuid import uuid4
from copy import deepcopy
from sqlalchemy.ext.declarative import declared_attr
import bcrypt

db = SQLAlchemy()

def generate_uid(jsn: dict):
    return str(uuid4())


class User(db.Model):
    """
    User of the application

    Parameters
    ---------
    uid: str
        Unique database id
    email: str
        user's unique email
    username: str
        user's unique username
    password: str
        user's password for login
    """
    uid = db.Column(db.String(255), primary_key=True, default=generate_uid)
    email = db.Column(db.String(255))
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(True), default=db.func.now())
    updated_at = db.Column(db.DateTime(True), default=db.func.now(), onupdate=db.func.now())

    def update_user(self, user_uid, new_info):
        user = db.session.query(User).filter_by(uid=user_uid).first()

        # check if values are the same before changing
        # ensure unique username and email for all users
        if user.username != new_info["username"]:
            if db.session.query(User).filter_by(username=new_info["username"]).first() is not None:
                return {"success": "False", "code": "400", "result": "Username already taken"}
            else:
                user.username = new_info["username"]

        if user.email != new_info["email"]:
            if db.session.query(User).filter_by(email=new_info["email"]).first() is not None:
                return {"success": "False", "code": "400", "result": "Email already taken"}
            else:
                user.email = new_info["email"]

        # password only has length if being changed
        if len(new_info["password"]):
            hashed = bcrypt.hashpw(new_info["password"].encode("utf-8"), bcrypt.gensalt())
            user.password = hashed.decode("utf-8")
        db.session.commit()
        return {"success": "True", "code": "200", "result": "User updated succesfully"}

    def to_json(self):
        return {"user_uid": self.uid,
                "username": self.username,
                "email": self.email}

class Employee(db.Model):
    """
    Calsse to represent an Employee in the application

    Parameters
    ---------
    uid: str
        Unique database id
    email: str
        employee's unique email
    first_name: str
        employee's unique first name
    last_name: str
        employee's unique last name
    age : int
       employee's age
    degree : str
        employee's degree
    entry_grade : str 
       employee's grade
    actual_grade : str 
       employee's actual grade
    next_grade : str 
       employee's next grade
    seniority : int
         employee's actual grade seniority in years
    """
    uid = db.Column(db.String(255), primary_key=True, default=generate_uid)
    email = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    social_situation = db.Column(db.String(255))
    entry_date = db.Column(db.DateTime(True))
    age = db.Column(db.Integer)
    degree = db.Column(db.String(255))
    grade = db.Column(db.String(255))
    grade_seniority = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(True), default=db.func.now())
    updated_at = db.Column(db.DateTime(True), default=db.func.now(), onupdate=db.func.now())

    def to_json(self):
        return {"user_uid": self.uid,
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "social_situation": self.social_situation,
                "entry_date": self.entry_date,
                "age": self.age,
                "degree": self.degree,
                "grade": self.grade,
                "grade_seniority": self.grade_seniority,
                "created_at": self.created_at,
                "updated_at": self.updated_at}

