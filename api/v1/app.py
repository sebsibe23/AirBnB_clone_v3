#!/usr/bin/python3
"""
Script that imports a Blueprint and runs Flask
"""
from flask import Flask, make_response, jsonify, abort
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_session(exception):
    """
    Closes the storage session
    """
    try:
        storage.close()
    except Exception as e:
        abort(500)


@app.errorhandler(404)
def not_found(error):
    """
    Returns a JSON response with a 404 status
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    try:
        HBNB_API_HOST = getenv('HBNB_API_HOST')
        HBNB_API_PORT = getenv('HBNB_API_PORT')

        host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        app.run(host=host, port=port, threaded=True)
    except Exception as e:
        abort(500)
