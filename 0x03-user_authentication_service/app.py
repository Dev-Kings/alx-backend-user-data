#!/usr/bin/env python3
"""
This is a simple web application that uses the Flask framework
to create a RESTful API.
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Bienvenue'})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
