import jwt
from flask import Flask, abort, request
from flask_restx import Api, Resource

from helpers.constants import ALGORITHM, SECRET


def login_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)
        return func(*args, **kwargs)

    return wrapper


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]

        try:
            jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        except Exception as err:
            print("JWT Decode Exception:", err)
            abort(401)
        return func(*args, **kwargs)

    return wrapper


app = Flask(__name__)
api = Api(app)

book_ns = api.namespace('')


@book_ns.route('/books/')
class BookView(Resource):

    def get(self):
        return [], 200

    @login_required
    def post(self):
        return '', 201


if __name__ == '__main__':
    app.run(debug=True)
