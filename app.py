"""
Main Flask Module
"""
from flask import Flask
from flask_restx import Api

from config import Config
from setup_db import db
from views.auth import auth_ns
from views.directors import directors_ns
from views.genres import genres_ns
from views.movies import movies_ns
from views.users import users_ns


def create_app(config_object: Config) -> Flask:
    """
    Create Flask application.
    """
    application = Flask(__name__)
    application.config.from_object(config_object)
    application.app_context().push()
    register_extensions(application)
    return application


def register_extensions(application: Flask) -> None:
    """
    Register extensions to the Flask application.
    """

    db.init_app(application)
    api = Api(application)
    namespaces = [directors_ns, genres_ns, movies_ns, users_ns, auth_ns]
    for namespace in namespaces:
        api.add_namespace(namespace)


app = create_app(Config())

if __name__ == '__main__':
    app.run()
