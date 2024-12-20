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


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """Get the user's profile"""
    session_id = request.cookies.get('session_id')

    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({'email': user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """Reset the user's password"""
    email = request.form.get('email')

    if not email:
        abort(403)

    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({'email': email, 'reset_token': reset_token}), 200


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """Update the user's password"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({'email': email, 'message': 'Password updated'}), 200


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
