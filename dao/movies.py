"""MoviesDAO module"""

from flask_restx import abort
from sqlalchemy.exc import NoResultFound

from dao.model.movies import Movies
from log_handler import dao_logger


class MoviesDAO:
    """
    Movies Data Access Object
    """

    def __init__(self, session):
        self.session = session
        self.logger = dao_logger

    def get_all_movies(self, year=None, did=None, gid=None):
        """
        Get all movies filtered or without filter
        :param year:    - filter by year
        :param did:     - filter by director_id
        :param gid:     - filter by genre_id
        :return:        - filtered movies
        """
        self.logger.info(
            'get_all_movies method called with parameters year=%s, did=%s, gid=%s',
            year, did, gid
        )
        all_movies = self.session.query(Movies)

        if year:
            all_movies = all_movies.filter(Movies.year == year)

        if did:
            all_movies = all_movies.filter(Movies.director_id == did)

        if gid:
            all_movies = all_movies.filter(Movies.genre_id == gid)

        all_movies = all_movies.all()
        self.logger.info(
            'get_all_movies method execution result: %s', all_movies
        )
        return all_movies

    def get_one_movie(self, mid):
        """
        Get one movie by Movie ID
        :param mid:     - movie_id
        :return:        - movie
        """
        self.logger.info('get_one_movie method called with parameter %s', mid)
        try:
            movie = self.session.query(Movies).filter(
                Movies.id == mid
            ).one()
        except NoResultFound as err:
            self.logger.error(
                "No movie found with id %d. Error: %s", mid, err
            )

            abort(404, f"No movie found with id {mid}. Error: {err}")
        self.logger.info('get_one_movie method execution result: %s', movie)
        return movie

    def post_movie(self, movie):
        """
        Add new movie to DB
        :param movie:   - movie data
        """
        self.logger.info('post_movie method called with parameter %s', movie)
        movie = Movies(**movie)
        self.session.add(movie)
        self.session.commit()
        self.logger.info('post_movie method execution result: %s', movie)

    def update_movie(self, mid, movie):
        """
        Update movie data by movie id
        :param mid:     - movie id
        :param movie:   - movie data for updating
        """
        self.logger.info(
            'update_movie method called with parameters mid=%s, movie=%s', mid,
            movie
        )
        result = self.session.query(Movies).filter(
            Movies.id == mid
        ).update(movie)

        self.session.commit()
        self.logger.info('update_movie method execution result: %s', result)
        return result

    def delete_movie(self, mid):
        """
        Delete movie by movie ID
        :param mid: - movie id
        """
        self.logger.info('delete_movie method called with parameter %s', mid)
        movie_data = self.get_one_movie(mid)
        self.session.delete(movie_data)
        self.session.commit()
        self.logger.info(
            'delete_movie method execution result: movie data with id=%s has been deleted',
            mid
        )
