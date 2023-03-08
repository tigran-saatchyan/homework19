"""Directors view module"""

from flask_restx import Namespace, Resource

from dao.model.directors import DirectorsSchema
from helpers.implemented import directors_service
from log_handler import views_logger

directors_ns = Namespace('directors')

directors_schema = DirectorsSchema(many=True)
director_schema = DirectorsSchema()


@directors_ns.route('/')
class DirectorsView(Resource):
    """
    DirectorsView Class Based View (CBV)
    """

    @staticmethod
    def get():
        """
        GET request handler for all directors
        :return:    - directors json
        """
        views_logger.info('Getting all directors...')
        directors = directors_service.get_directors()
        views_logger.info('Returned %s directors', len(directors))
        return directors_schema.dump(directors), 200


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    """
    DirectorView Class Based View (CBV)
    """

    @staticmethod
    def get(did):
        """
        GET request handler for one director by director id
        :param did:     - director id
        :return:        - director json
        """
        views_logger.info('Getting director with id %d...', did)
        director = directors_service.get_one_director(did)
        views_logger.info('Returned director: %s', director)
        return director_schema.dump(director), 200
