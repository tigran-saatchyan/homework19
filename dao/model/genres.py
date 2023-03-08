"""Genres model and schema module"""

from marshmallow import Schema, fields

from setup_db import db


class Genres(db.Model):
    """
    Genres model
    """
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f'Genre: {self.id} - {self.name}'


class GenresSchema(Schema):
    """
    Genres schema
    """
    id = fields.Int()
    name = fields.Str()
