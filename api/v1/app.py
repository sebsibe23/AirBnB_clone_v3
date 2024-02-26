#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""

from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from models import storage
import os
from werkzeug.exceptions import HTTPException

# Global Flask Application Variable: app
app = Flask(__name__)
swagger = Swagger(app)

# global strict slashes
app.url_map.strict_slashes = False

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# Cross-Origin Resource Sharing
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """
    After each request, this method calls .close() on the current
    SQLAlchemy Session.

    Parameters:
        exception: The exception raised (unused).

    Exceptions:
        None.
    """
    try:
        storage.close()
    except Exception as e:
        print(f"An error occurred during teardown_db: {str(e)}")


@app.errorhandler(404)
def handle_404(exception):
    """
    Handles 404 errors, in the event that global error handler fails.

    Parameters:
        exception: The exception raised.

    Exceptions:
        None.
    """
    try:
        code = exception.__str__().split()[0]
        description = exception.description
        message = {'error': description}
        return make_response(jsonify(message), code)
    except Exception as e:
        print(f"An error occurred during handle_404: {str(e)}")


@app.errorhandler(400)
def handle_400(exception):
    """
    Handles 400 errors, in the event that global error handler fails.

    Parameters:
        exception: The exception raised.

    Exceptions:
        None.
    """
    try:
        code = exception.__str__().split()[0]
        description = exception.description
        message = {'error': description}
        return make_response(jsonify(message), code)
    except Exception as e:
        print(f"An error occurred during handle_400: {str(e)}")


@app.errorhandler(Exception)
def global_error_handler(err):
    """
    Global route to handle all error status codes.

    Parameters:
        err: The exception raised.

    Exceptions:
        None.
    """
    try:
        if isinstance(err, HTTPException):
            if type(err).__name__ == 'NotFound':
                err.description = "Not found"
            message = {'error': err.description}
            code = err.code
        else:
            message = {'error': err}
            code = 500
        return make_response(jsonify(message), code)
    except Exception as e:
        print(f"An error occurred during global_error_handler: {str(e)}")


def setup_global_errors():
    """
    Updates HTTPException Class with custom error function.

    Parameters:
        None.

    Exceptions:
        None.
    """
    try:
        for cls in HTTPException.__subclasses__():
            app.register_error_handler(cls, global_error_handler)
    except Exception as e:
        print(f"An error occurred during setup_global_errors: {str(e)}")


if __name__ == "__main__":
    """
    MAIN Flask App
    """
    try:
        setup_global_errors()
        app.run(host=host, port=port)
    except Exception as e:
        print(f"An error occurred during Flask app execution: {str(e)}")
