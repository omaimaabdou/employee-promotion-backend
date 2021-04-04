from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass, field
from typing import List, Union, TypeVar, Type, Optional
from uuid import uuid4
from copy import deepcopy
from sqlalchemy.ext.declarative import declared_attr

db = SQLAlchemy()

def generate_uid(jsn: dict):
    return str(uuid4())


class User(db.Model):
    """
    User of the application

    Parameters
    ---------
    uid: int
        Unique database id
    email: str
        user's unique email
    username: str
        user's unique username
    password: str
        user's password for login
    subscription: str
        subscription plan associated with user account
    """
    id: int = db.Column(db.String(120), primary_key=True, default=generate_uid)
    email: str = db.Column(db.String(255))
    username: str = db.Column(db.String(255))
    password: str = db.Column(db.String(255))
    subscription: str = db.Column(db.String(255))
