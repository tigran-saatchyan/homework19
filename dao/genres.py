"""GenresDAO module"""

from dao.model.genres import Genres
from log_handler import dao_logger


class GenresDAO:
    """
    Genre Data Access Object
    """

    def __init__(self, session):
        self.session = session
        self.logger = dao_logger

    def get_all_genres(self):
        """
        Get all genres from DB
        :return:    -   all genres
        """
        self.logger.info('get_all_genres method called')
        genres = self.session.query(Genres).all()
        self.logger.info('get_all_genres method execution result: %s', genres)
        return genres

    def get_one_genre(self, gid):
        """
        Get one genre by Genre ID (gid)
        :param gid:     - genre ID
        :return:        - one genre
        """
        self.logger.info('get_one_genre method called with parameter %s', gid)
        genre = self.session.query(Genres).filter(
            Genres.id == gid
        ).one()
        self.logger.info('get_one_genre method execution result: %s', genre)
        return genre

    def post_genre(self, genre):
        """
        Insert new genre to DB
        :param genre:   -   genre data
        """
        self.logger.info('post_genre method called with parameter %s', genre)
        genre = Genres(**genre)
        self.session.add(genre)
        self.session.commit()
        self.logger.info('post_genre method execution result: %s', genre)
