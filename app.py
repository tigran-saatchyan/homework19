"""Main Flask Module"""
from flask import Flask
from flask_restx import Api

from config import Config
from setup_db import db
from views.directors import directors_ns
from views.genres import genres_ns
from views.movies import movies_ns


def create_app(config_object: Config) -> Flask:
    """
    Create a Flask app
    :param config_object:   - flask config object
    :return:                - configured Flask app
    """
    application = Flask(__name__)
    application.config.from_object(config_object)
    application.app_context().push()
    register_extensions(application)
    return application


def register_extensions(application):
    """
    Registering extensions for Flask app
    :param application:     - Flask app
    """
    db.init_app(application)
    api = Api(application)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(movies_ns)


app = create_app(Config())

if __name__ == '__main__':
    app.run()
