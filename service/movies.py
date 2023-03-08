"""Movies Service module"""

from dao.model.movies import Movies
from dao.movies import MoviesDAO
from log_handler import services_logger


class MoviesService:
    """
    Movies Service class
    """

    def __init__(self, movies_dao: MoviesDAO):
        self.movies_dao = movies_dao
        self.logger = services_logger

    def get_all_movies(self, year, did, gid):
        """
        Get all movies filtered or without filter
        :param year:    - filter by year
        :param did:     - filter by director_id
        :param gid:     - filter by genre_id
        :return:        - filtered movies
        """
        self.logger.info("Retrieving all movies")
        movies = self.movies_dao.get_all_movies(year, did, gid)
        self.logger.info(f"Retrieved {len(movies)} movies")
        return movies

    def get_one_movie(self, mid):
        """
        Get one movie by Movie ID
        :param mid:     - movie_id
        :return:        - movie
        """
        self.logger.info(f"Retrieving movie with ID {mid}")
        return self.movies_dao.get_one_movie(mid)

    def post_movie(self, movie):
        """
        Add new movie to DB
        :param movie:   - movie data
        """
        self.logger.info("Adding a new movie")
        return self.movies_dao.post_movie(movie)

    def update_movie(self, mid, movie):
        """
        Update movie data by movie id
        :param mid:     - movie id
        :param movie:   - movie data for updating
        """
        count_columns = Movies.__table__.columns
        if len(count_columns) - 1 != len(movie.keys()):
            self.logger.error(
                "Failed to update movie: Invalid number of columns"
            )
            return
        self.logger.info(f"Updating movie with ID {mid}")
        result = self.movies_dao.update_movie(mid, movie)
        self.logger.info(f"Updated {result} rows")
        return result

    def delete_movie(self, mid):
        """
        Delete movie by movie ID
        :param mid: - movie id
        :return:    - None
        """
        self.logger.info(f"Deleting movie with ID {mid}")
        self.movies_dao.delete_movie(mid)
