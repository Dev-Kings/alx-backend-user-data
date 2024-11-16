#!/usr/bin/env python3
"""Session authentication views"""
from flask import jsonify, request, abort
from api.v1.app import auth
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route(
        '/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    POST /auth_session/login
    Handles session authentication
    """
    # Import only within the function to avoid circular import issues
    from api.v1.app import auth

    # Retrieve the email and password from the request
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate the email
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Validate the password
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Search for user by email
    users = User.search({'email': email})
    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]

    # Validate the password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create a session cookie
    session_id = auth.create_session(user.id)

    # Prepare the response
    user_json = user.to_json()
    response = jsonify(user_json)

    # Set the session cookie
    session_name = getenv('SESSION_NAME', '_my_session_id')
    response.set_cookie(session_name, session_id)

    return response


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """
    DELETE /api/v1/auth_session/logout
    Handles logout by deleting session
    """
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
