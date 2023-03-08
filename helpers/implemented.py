"""Implementation module"""

from dao.directors import DirectorsDAO
from dao.genres import GenresDAO
from dao.movies import MoviesDAO
from service.directors import DirectorsService
from service.genres import GenresService
from service.movies import MoviesService
from setup_db import db

directors_dao = DirectorsDAO(db.session)
directors_service = DirectorsService(directors_dao)

genres_dao = GenresDAO(db.session)
genres_service = GenresService(genres_dao)

movies_dao = MoviesDAO(db.session)
movies_service = MoviesService(movies_dao)

users_dao = UsersDAO(db.session)
users_service = UsersService(users_dao)
