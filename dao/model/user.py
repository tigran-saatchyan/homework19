"""User model module"""
from marshmallow import Schema, fields

from setup_db import db


class User(db.Model):
    """
    User model
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    role = db.Column(db.String, default='user')

    def __repr__(self):
        return f'User: {self.username}'


class UserSchema(Schema):
    """
    User model
    """
    id = fields.Int(dump_only=True)
    username = fields.Str()
    role = fields.Str()

    class Meta:
        ordered = True
