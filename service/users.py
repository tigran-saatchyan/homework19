"""User Service module"""
import base64
import hashlib
import hmac

from flask import abort

from dao.users import UserDAO
from helpers.constants import CRYPTOGRAPHIC_HASH_FUNCTION, \
    PWD_HASH_ITERATIONS, PWD_HASH_SALT
from log_handler import services_logger


class UserService:
    """
    UserService class provides methods to interact with the UserDAO.

    :param users_dao: A UserDAO object to use for database interaction.
    """

    def __init__(self, users_dao: UserDAO):
        self.users_dao = users_dao
        self.logger = services_logger

    def get_all(self):
        """
        Retrieve all users.

        :return: A list of all users.
        """
        self.logger.info('Retrieving all users')
        return self.users_dao.get_all()

    def get_one(self, uid):
        """
        Retrieve a user by ID.

        :param uid: The ID of the user to retrieve.

        :return: The user with the specified ID.
        """
        self.logger.info(f'Retrieving user with ID {uid}')
        return self.users_dao.get_one(uid)

    def get_by_username(self, username):
        """
        Retrieve a user by username.

        :param username: The username of the user to retrieve.

        :return: The user with the specified username.
        """
        self.logger.info(f'Retrieving user with username {username}')
        return self.users_dao.get_by_username(username)

    def create(self, user_data):
        """
        Create a new user.

        :param user_data: A dictionary containing the details of the new user.

        :return: The ID of the newly created user.
        """
        self.logger.info('Adding new user')

        user = self.get_by_username(user_data["username"])
        if user is not None:
            abort(400, f"user with username '{user.username}' already exists")
        user_data["password"] = self.hash_password(
            user_data.get("password")
        )
        return self.users_dao.create(user_data)

    def update(self, uid, user_data):
        """
        Update an existing user.

        :param uid: The ID of the user to update.
        :param user_data: A dictionary containing the updated details
            of the user.

        :return: The number of rows affected by the update.
        """
        self.logger.info('Updating user data')
        user_data["password"] = self.hash_password(
            user_data.get("password")
        )
        return self.users_dao.update(uid, user_data)

    def delete(self, uid):
        """
        Delete a user.

        :param uid: The ID of the user to delete.
        """
        self.logger.info(f"Deleting user with ID {uid}")
        self.users_dao.delete(uid)

    @staticmethod
    def hash_password(password):
        """
        Hash a password using a cryptographic hash function.

        :param password: The password to hash.

        :return: The hashed password.
        """
        return base64.b64encode(
            hashlib.pbkdf2_hmac(
                CRYPTOGRAPHIC_HASH_FUNCTION,
                password.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            )
        )

    @staticmethod
    def compare_passwords(db_pwd, received_pwd) -> bool:
        """
        Compares two passwords for equality.

        :param db_pwd: A base64 encoded hashed password string from
            the database.
        :param received_pwd: A plain text password string received from
            the user.

        :return: A boolean indicating whether the passwords match.
        """
        return hmac.compare_digest(
            base64.b64decode(db_pwd),
            hashlib.pbkdf2_hmac(
                CRYPTOGRAPHIC_HASH_FUNCTION,
                received_pwd.encode('utf-8'),
                PWD_HASH_SALT,
                PWD_HASH_ITERATIONS
            )
        )
