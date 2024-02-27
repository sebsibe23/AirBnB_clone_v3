#!/usr/bin/python3
"""
Flask route that returns JSON status response
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
    Function for the status route that returns the status
    """
    try:
        if request.method == 'GET':
            resp = {"status": "OK"}
            return jsonify(resp)
    except Exception as e:
        # Handle specific exception or log the error
        pass


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Function to return the count of all class objects
    """
    try:
        if request.method == 'GET':
            response = {}
            PLURALS = {
                "Amenity": "amenities",
                "City": "cities",
                "Place": "places",
                "Review": "reviews",
                "State": "states",
                "User": "users"
            }
            for key, value in PLURALS.items():
                response[value] = storage.count(key)
            return jsonify(response)
    except Exception as e:
        # Handle specific exception or log the error
        pass
