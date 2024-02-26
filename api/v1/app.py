#!/usr/bin/python3
"""
Flask server that handles API requests and responses.
"""

from flask import Flask, jsonify
from models import storage
from os import getenv
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

# Create a CORS instance
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.teardown_appcontext
def downtear(self):
    """
    Closes the database connection at the end of each request.
    """
    try:
        storage.close()
    except Exception as e:
        return jsonify(error=str(e)), 500


@app.errorhandler(404)
def page_not_found(error):
    """
    Handles 404 errors and returns a JSON response with
    the message "Not found".
    """
    return jsonify(error='Not found'), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host=host, port=port, threaded=True)
