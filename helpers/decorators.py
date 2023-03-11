"""Decorators module"""
from functools import wraps

import jwt
from flask import abort, request

from helpers.constants import JWT_ALGORITHM, JWT_SECRET
from log_handler import views_logger


def auth_required(func):
    """
    A decorator that checks if the request contains a valid JWT access
    token in the Authorization header. If the token is invalid or
    missing, returns a 401 Unauthorized error.

    :param func:    - the function to be decorated
    :return:        - the decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]

        try:
            jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except Exception as err:
            print("JWT Decode Exception:", err)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    """
    A decorator that checks if the request contains a valid JWT access
    token with the 'admin' role in the Authorization header. If the
    token is invalid or missing, or the user doesn't have the 'admin'
    role, returns a 401 Unauthorized or 403 Forbidden error.

    :param func:    - the function to be decorated
    :return:        - the decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        role = None

        try:
            user = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            role = user.get('role', 'user')
        except Exception as err:
            print("JWT Decode Exception:", err)
            abort(401)

        if role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper


def put_logging_and_response(func):
    """
    A decorator that logs the request method and URL, calls the
    decorated function, and logs the response. If the function returns a
    truthy value, logs a 'Success' response; otherwise, returns a 400 Bad
    Request error with a 'must contain all required fields' message.

    :param func:    - the function to be decorated
    :return:        - the decorated function
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        views_logger.info(
            'Request received: %s %s',
            request.method, request.url
        )
        result = func(*args, **kwargs)
        if result:
            views_logger.info('Response sent: Success')
            return "Success", 200

        views_logger.warning(
            'Response sent: must contain all required fields'
        )
        abort(400, {"error": "must contain all required fields"})

    return wrapper
