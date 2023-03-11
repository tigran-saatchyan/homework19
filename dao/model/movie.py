"""Movie model and schema module"""

from marshmallow import Schema, fields
from sqlalchemy.orm import relationship

from dao.model.director import Director
from dao.model.genre import Genre
from setup_db import db


class Movie(db.Model):
    """
    Movie model
    """
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    trailer = db.Column(db.Integer)
    year = db.Column(db.Integer)
    rating = db.Column(db.String)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    director_id = db.Column(db.Integer, db.ForeignKey('director.id'))

    genre = relationship(Genre)
    director = relationship(Director)

    def __repr__(self):
        return f'Movie: {self.title} - {self.year} - {self.rating}'


class MovieSchema(Schema):
    """
    Movie schema
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
