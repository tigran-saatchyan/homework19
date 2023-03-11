"""UserDAO module"""

from dao.model.user import User
from log_handler import dao_logger


class UserDAO:

    def __init__(self, session):
        """
        Constructor method.

        :param session: The session object to use for database interaction.
        """
        self.session = session
        self.logger = dao_logger

    def get_all(self):
        """
        Retrieve all users in the User table.

        :return: A list of User objects.
        """
        self.logger.info('get_all users method called')
        users = self.session.query(User).all()
        self.logger.info('get_all users method execution result: %s', users)
        return users

    def get_one(self, uid):
        """
        Retrieve a single user from the User table by their ID.

        :param uid: The ID of the user to retrieve.

        :return: A User object.
        """
        self.logger.info(
            'get_one user method called with parameter %s', uid
        )
        user = self.session.query(User).filter(
            User.id == uid
        ).one()
        self.logger.info(
            'get_one user method execution result: %s', user
        )
        return user

    def get_by_username(self, username):
        """
        Retrieve a single user from the User table by their username.

        :param username: The username of the user to retrieve.

        :return: A User object.
        """
        self.logger.info(
            'get_by_username method called with parameter %s', username
        )
        user = self.session.query(User).filter(
            User.username == username
        ).first()
        self.logger.info(
            'get_by_username method execution result: %s', user
        )
        return user

    def create(self, user_data):
        """
        Create a new user in the User table.

        :param user_data: A dictionary containing the user data.

        :return: A User object representing the newly created user.
        """
        self.logger.info(
            'create user method called with parameter %s', user_data
        )
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        self.logger.info('create user method execution result: %s', user)
        return user

    def delete(self, uid):
        """
        Delete a user from the User table by their ID.

        :param uid: The ID of the user to delete.
        """
        user = self.get_one(uid)
        self.session.delete(user)
        self.session.commit()

        self.logger.info(f"User with id {uid} has been deleted.")

    def update(self, uid, user_data):
        """
        Update an existing user in the User table.

        :param uid: The ID of the user to update.
        :param user_data: A dictionary containing the new user data.
        """
        user = self.get_one(uid)
        user.username = user_data.get("username")
        user.password = user_data.get("password")

        self.session.add(user)
        self.session.commit()

        self.logger.info(
            f"User with id {user.id} has been updated with new "
            f"username and password."
        )
