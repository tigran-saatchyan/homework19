"""Implementation module"""

from dao.directors import DirectorDAO
from dao.genres import GenreDAO
from dao.movies import MovieDAO
from dao.users import UserDAO
from service.auth import AuthService
from service.directors import DirectorService
from service.genres import GenreService
from service.movies import MovieService
from service.users import UserService
from setup_db import db

directors_dao = DirectorDAO(db.session)
directors_service = DirectorService(directors_dao)

genres_dao = GenreDAO(db.session)
genres_service = GenreService(genres_dao)

movies_dao = MovieDAO(db.session)
movies_service = MovieService(movies_dao)

user_dao = UserDAO(db.session)
user_service = UserService(user_dao)

auth_service = AuthService(user_service)
