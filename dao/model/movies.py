"""Movies model and schema module"""

from marshmallow import Schema, fields
from sqlalchemy.orm import relationship

from dao.model.directors import Directors
from dao.model.genres import Genres
from setup_db import db


class Movies(db.Model):
    """
    Movies model
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    trailer = db.Column(db.Integer)
    year = db.Column(db.Integer)
    rating = db.Column(db.String)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'))

    genre = relationship(Genres)
    director = relationship(Directors)

    def __repr__(self):
        return f'Movie: {self.title} - {self.year} - {self.rating}'


class MoviesSchema(Schema):
    """
    Movies schema
    """
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Str()
    genre_id = fields.Int()
    director_id = fields.Int()

    class Meta:
        ordered = True
