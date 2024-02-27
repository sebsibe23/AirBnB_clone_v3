#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, render_template, url_for
from models import storage
import os
from werkzeug.exceptions import HTTPException

# Global Flask Application Variable: app
app = Flask(__name__)

# global strict slashes
app.url_map.strict_slashes = False

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)


# begin flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """
    After each request, this method calls .close() (i.e., .remove()) on
    the current SQLAlchemy Session
    """
    try:
        storage.close()
    except Exception as e:
        # Handle specific exception or log the error
        pass


@app.errorhandler(404)
def handle_404(exception):
    """
    Handles 404 errors, in the event that global error handler fails
    """
    try:
        code = exception.__str__().split()[0]
        description = exception.description
        message = {'error': description}
        return make_response(jsonify(message), code)
    except Exception as e:
        # Handle specific exception or log the error
        pass


@app.errorhandler(400)
def handle_404(exception):
    """
    Handles 400 errors, in the event that global error handler fails
    """
    try:
        code = exception.__str__().split()[0]
        description = exception.description
        message = {'error': description}
        return make_response(jsonify(message), code)
    except Exception as e:
        # Handle specific exception or log the error
        pass


@app.errorhandler(Exception)
def global_error_handler(err):
    """
    Global route to handle all error status codes
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
        # Handle specific exception or log the error
        pass


def setup_global_errors():
    """
    Updates HTTPException Class with custom error function
    """
    try:
        for cls in HTTPException.__subclasses__():
            app.register_error_handler(cls, global_error_handler)
    except Exception as e:
        # Handle specific exception or log the error
        pass


if __name__ == "__main__":
    """
    MAIN Flask App
    """
    try:
        # Initializes global error handling
        setup_global_errors()
        # Start Flask app
        app.run(host=host, port=port)
    except Exception as e:
        # Handle specific exception or log the error
        pass
