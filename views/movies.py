"""Movies view module"""

from flask import request
from flask_restx import Api, Namespace, Resource, reqparse
from werkzeug.exceptions import HTTPException

from dao.model.movies import MoviesSchema
from helpers.implemented import movies_service
from log_handler import views_logger

movies_ns = Namespace('movies')

movies_schema = MoviesSchema(many=True)
movie_schema = MoviesSchema()

api = Api()

movies_parser = reqparse.RequestParser()
movies_parser.add_argument(
    'year',
    type=int,
    help='(optional) Filter by year'
)

movies_parser.add_argument(
    'director_id',
    type=int,
    help='(optional) Filter by director ID:'
)

movies_parser.add_argument(
    'genre_id',
    type=int,
    help='(optional) Filter by genre ID:'
)


@movies_ns.route('/')
class MoviesView(Resource):
    """
    MoviesView Class Based View (CBV)
    """

    @api.doc(parser=movies_parser)
    @movies_ns.response(200, 'Success')
    @movies_ns.response(400, 'Bad Request')
    def get(self):
        """
        GET request handler for all movies with or without filter
        :return:    - movies json and response code
        """
        views_logger.info(
            'Request received: %s - %s',
            request.method, request.url
        )
        params = ['year', 'director_id', 'genre_id']
        errors = {
            param: f"{param.title()} must be a digital value" for param
            in params if
            request.args.get(param) and not request.args.get(
                param
            ).isdigit()
        }

        if errors:
            views_logger.warning('Invalid request parameters: %s', errors)
            return errors, 400

        year, director_id, genre_id = (
            request.args.get(param, 0, type=int)
            for param in params
        )

        movies = movies_service.get_all_movies(year, director_id, genre_id)
        response = movies_schema.dump(movies)
        views_logger.info('Response sent: %s', response)
        return response, 200

    @staticmethod
    def post():
        """
        POST request handler to add movie in db with data from
        request body
        {
            "title": str,
            "description": str,
            "trailer": str,
            "year": int,
            "rating": str,
            "genre_id": int,
            "director_id": int
        }
        :return:    - empty string and response code
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        movie = request.json
        movies_service.post_movie(movie)
        views_logger.info('Response sent: Success')
        return "", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    """
    MovieView Class Based View (CBV)
    """

    @staticmethod
    @movies_ns.response(200, 'Success')
    @movies_ns.response(404, 'Not Found')
    def get(mid):
        """
        GET request handler for movie by pk
        :param mid:     - movie id
        :return:        - movie json and response code
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        try:
            movie = movies_service.get_one_movie(mid)
        except HTTPException as err:
            views_logger.error(
                "Error retrieving movie with id %d. Error: %s",
                mid, err
            )
            return {'message': err.description}, err.code

        response = movie_schema.dump(movie)
        views_logger.info('Response sent: %s', response)
        return response, 200

    @staticmethod
    @movies_ns.response(200, 'Success')
    @movies_ns.response(204, 'No Content')
    def put(mid):
        """
        PUT request handler for movie by pk to update movie data
        by received movie data in request body
        {
            "title": str,
            "description": str,
            "trailer": str,
            "year": int,
            "rating": str,
            "genre_id": int,
            "director_id": int
        }
        :param mid:     - movie id
        :return:        - response and response code
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        movie = request.json
        result = movies_service.update_movie(mid, movie)
        if result:
            views_logger.info('Response sent: Success')
            return "Success", 200
        views_logger.warning(
            'Response sent: must contain all required fields'
        )
        return {"error": "must contain all required fields"}, 204

    @staticmethod
    @movies_ns.response(204, 'No Content')
    @movies_ns.response(404, 'Not Found')
    def delete(mid):
        """
        DELETE request handler to delete movie by id
        :param mid:     - movie id
        :return:        - empty string and response code
        """
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        movies_service.delete_movie(mid)
        views_logger.info('Response sent: No Content')
        return "", 204
