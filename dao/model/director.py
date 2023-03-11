"""Director model and schema module"""
from dataclasses import dataclass

from marshmallow import Schema, fields

from setup_db import db


@dataclass
class Director(db.Model):
    """
    Director model
    """
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    def __repr__(self):
        return 'Director: %s - %s', self.id, self.name


class DirectorSchema(Schema):
    """
    Director schema with id set to dump_only
    """
    id = fields.Int(dump_only=True)
    name = fields.Str()
