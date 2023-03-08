"""Genres view module"""

from flask_restx import Namespace, Resource

from dao.model.genres import GenresSchema
from helpers.implemented import genres_service
from log_handler import views_logger

genres_ns = Namespace('genres')

genres_schema = GenresSchema(many=True)
genre_schema = GenresSchema()


@genres_ns.route('/')
class GenresView(Resource):
    """
    GenresView Class Based View (CBV)
    """

    @staticmethod
    def get():
        """
        GET request handler for all genres
        :return:    - genres json
        """
        views_logger.info('Retrieving all genres')
        genres = genres_service.get_all_genres()
        views_logger.debug('Retrieved %s genres', len(genres))
        return genres_schema.dump(genres), 200


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    """
    GenreView Class Based View (CBV)
    """

    @staticmethod
    def get(gid):
        """
        GET request handler for one genre by id
        :return:    - genre json
        """
        views_logger.info('Retrieving genre with id %s', gid)
        genre = genres_service.get_one_genre(gid)

        if genre:
            views_logger.debug('Retrieved genre: %s', genre)
            return genre_schema.dump(genre), 200

        views_logger.warning('Genre with id %s not found', gid)
        return {'message': 'Genre not found'}, 404
