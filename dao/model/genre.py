"""Genre model and schema module"""

from marshmallow import Schema, fields

from setup_db import db


class Genre(db.Model):
    """
    Genre model
    """
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f'Genre: {self.id} - {self.name}'


class GenreSchema(Schema):
    """
    Genre schema
    """
    id = fields.Int()
    name = fields.Str()
