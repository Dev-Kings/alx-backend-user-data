#!/usr/bin/env python3
"""
This is a simple web application that uses the Flask framework
to create a RESTful API.
"""

from flask import Flask, jsonify, request
from auth import Auth


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
        return jsonify({'email': user.email, 'message': 'user created'}), 201
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
