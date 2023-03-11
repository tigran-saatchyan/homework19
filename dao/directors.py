"""DirectorDAO module"""

from dao.model.director import Director
from log_handler import dao_logger


class DirectorDAO:
    """
    Data access object for Director model.
    """

    def __init__(self, session):
        """
        Constructor method.

        :param session: - The session object to use for database interaction.
        """
        self.session = session
        self.logger = dao_logger

    def get_all(self):
        """
        Get all the directors from the database.

        :return:    - A list of Director objects.
        """
        self.logger.info('get_all directors method called')
        directors = self.session.query(Director).all()
        self.logger.info(
            'get_all_directors method execution result: %s', directors
        )
        return directors

    def get_one(self, did):
        """
        Get a single director from the database.

        :param did:     - The id of the director to retrieve.

        :return:        - A Director object.
        """
        self.logger.info(
            'get_one_director method called with parameter %s', did
        )
        director = self.session.query(Director).filter(
            Director.id == did
        ).first()
        self.logger.info(
            f'get_one_director method execution result: {director.name}'
        )
        return director

    def create(self, director):
        """
        Create a new director in the database.

        :param director:  - A dictionary containing the details of the
        director to create.
        """
        self.logger.info(
            'create method called with parameter %s', director
        )

        director = Director(**director)
        self.session.add(director)
        self.session.commit()
        self.logger.info(
            f'create method execution result: {director}'
        )

    def delete(self, did):
        """
        Delete a director from the database.

        :param did:     - The id of the director to delete.
        """
        director = self.get_one(did)
        self.session.delete(director)
        self.session.commit()

        self.logger.info(f"Director with id {did} has been deleted.")

    def update(self, did, director_data):
        """
        Update the details of a director in the database.

        :param did:           - The id of the director to update.
        :param director_data: - A dictionary containing the details to update.

        :return:              - The number of rows updated.
        """
        row_updated = self.session.query(Director).filter(
            Director.id == did
        ).update({"name": director_data.get("name")})

        self.session.commit()

        if row_updated:
            self.logger.info(
                f"{Director.__name__} with id {did} has been updated "
                f"with new name - {director_data.get('name')}. "
                f"Rows updated - {row_updated}"
            )
        return row_updated
