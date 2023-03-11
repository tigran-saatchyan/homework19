"""MovieDAO module"""

from flask_restx import abort
from sqlalchemy.exc import NoResultFound

from dao.model.movie import Movie
from log_handler import dao_logger


class MovieDAO:

    def __init__(self, session):
        """
        Constructor method.

        :param session: The session object to use for database interaction.
        """
        self.session = session
        self.logger = dao_logger

    def get_all(self, year=None, did=None, gid=None):
        """
        Retrieve all movies from the database with the option to filter by
        year, director ID, or genre ID.

        :param year: An optional integer representing the year the movie was
            released.
        :param did: An optional integer representing the ID of the movie's
            director.
        :param gid: An optional integer representing the ID of the movie's
            genre.

        :return: A list of Movie objects.
        """
        self.logger.info(
            'get_all_movies method called with parameters '
            'year=%s, did=%s, gid=%s',
            year, did, gid
        )
        all_movies = self.session.query(Movie)

        if year:
            all_movies = all_movies.filter(Movie.year == year)

        if did:
            all_movies = all_movies.filter(Movie.director_id == did)

        if gid:
            all_movies = all_movies.filter(Movie.genre_id == gid)

        all_movies = all_movies.all()
        self.logger.info(
            'get_all_movies method execution result: %s', all_movies
        )
        return all_movies

    def get_one(self, mid):
        """
        Retrieve a single movie from the database by its ID.

        :param mid: An integer representing the ID of the movie to retrieve.

        :return: A Movie object.
        """
        self.logger.info('get_one_movie method called with parameter %s', mid)
        try:
            movie = self.session.query(Movie).filter(
                Movie.id == mid
            ).one()
        except NoResultFound as err:
            self.logger.error(
                "No movie found with id %d. Error: %s", mid, err
            )
            abort(404, f"No movie found with id {mid}. Error: {err}")
        self.logger.info('get_one_movie method execution result: %s', movie)
        return movie

    def create(self, movie):
        """
        Create a new movie in the database.

        :param movie: A dictionary representing the movie to create, with keys
            corresponding to column names in the Movie table.
        """
        self.logger.info('post_movie method called with parameter %s', movie)
        movie = Movie(**movie)
        self.session.add(movie)
        self.session.commit()
        self.logger.info('post_movie method execution result: %s', movie)

    def update(self, mid, movie):
        """
        Update an existing movie in the database.

        :param mid: An integer representing the ID of the movie to update.
        :param movie: A dictionary representing the updated movie data, with
            keys corresponding to column names in the Movie table.

        :return: The number of rows updated in the database.
        """
        self.logger.info(
            'update_movie method called with parameters mid=%s, movie=%s', mid,
            movie
        )
        result = self.session.query(Movie).filter(
            Movie.id == mid
        ).update(movie)

        self.session.commit()
        self.logger.info('update_movie method execution result: %s', result)
        return result

    def delete(self, mid):
        """
        Delete a movie data from the database with the given id.

        :param mid: An integer representing the id of the movie to be deleted.
        """
        self.logger.info('delete_movie method called with parameter %s', mid)
        movie = self.get_one(mid)
        self.session.delete(movie)
        self.session.commit()
        self.logger.info(
            'delete_movie method execution result: movie data '
            'with id=%s has been deleted',
            mid
        )
