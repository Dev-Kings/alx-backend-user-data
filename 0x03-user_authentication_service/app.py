#!/usr/bin/env python3
"""
This is a simple web application that uses the Flask framework
to create a RESTful API.
"""

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect, url_for


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def hello() -> str:
    """
    This function is the starting point of the application.
    """
    return jsonify({'message': 'Bienvenue'})


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """
    This function registers a new user.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({'email': user.email, 'message': 'user created'}), 200
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """Login the user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400)

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({'email': email, 'message': 'logged in'})
        response.set_cookie('session_id', session_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """Logout the user"""
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    response = redirect(url_for('hello'))
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
