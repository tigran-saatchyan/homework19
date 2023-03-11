"""GenreDAO module"""

from dao.model.genre import Genre
from log_handler import dao_logger


class GenreDAO:
    """
    A data access object (DAO) class for interacting with the Genre
    table in the database.

    :param session: The SQLAlchemy session object to use for database
    interactions.
    """
    def __init__(self, session):
        """
        Constructor method.

        :param session: The session object to use for database interaction.
        """
        self.session = session
        self.logger = dao_logger

    def get_all(self):
        """
        Retrieve all genres from the database.

        :return: A list of Genre objects representing all genres in the database.
        """
        self.logger.info('get_all_genres method called')
        genres = self.session.query(Genre).all()
        self.logger.info('get_all_genres method execution result: %s', genres)
        return genres

    def get_one(self, gid):
        """
        Retrieve a single genre from the database by its id.

        :param gid: The id of the genre to retrieve.

        :return: A Genre object representing the genre with the specified id.
        """
        self.logger.info('get_one_genre method called with parameter %s', gid)
        genre = self.session.query(Genre).filter(
            Genre.id == gid
        ).one()
        self.logger.info('get_one_genre method execution result: %s', genre)
        return genre

    def create(self, genre):
        """
        Create a new genre in the database.

        :param genre: A dictionary containing the data for the new genre.
        """
        self.logger.info('post_genre method called with parameter %s', genre)
        genre = Genre(**genre)
        self.session.add(genre)
        self.session.commit()
        self.logger.info('post_genre method execution result: %s', genre)

    def delete(self, gid):
        """
        Delete a genre from the database.

        :param gid: The id of the genre to delete.
        """
        genre = self.get_one(gid)
        self.session.delete(genre)
        self.session.commit()

        self.logger.info(f"Genre with id {gid} has been deleted.")

    def update(self, gid, genre_data):
        """
        Update the name of a genre in the database.

        :param gid: The id of the genre to update.
        :param genre_data: A dictionary containing the new name of the genre.

        :return: The number of rows updated in the database.
        """
        row_updated = self.session.query(Genre).filter(
            Genre.id == gid
        ).update({"name": genre_data.get("name")})

        self.session.commit()

        if row_updated:
            self.logger.info(
                f"Genre with id {gid} has been updated with new name "
                f"- {genre_data.get('name')}. Rows updated - {row_updated}"
            )
        return row_updated
