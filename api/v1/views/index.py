#!/usr/bin/python3
"""
API Routes for status and statistics endpoints
"""

import models
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify, request, Blueprint
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """
    Route that returns the status of the API
    """
    try:
        if request.method == 'GET':
            response = {"status": "OK"}
            return jsonify(response)
    except Exception as e:
        return jsonify(error=str(e)), 500


@app_views.route('/stats', methods=['GET'])
def stats():
    """
    Route that returns the count of objects for each class
    """
    try:
        if request.method == 'GET':
            response = {}
            class_names = {
                "Amenity": "amenities",
                "City": "cities",
                "Place": "places",
                "Review": "reviews",
                "State": "states",
                "User": "users"
            }
            for class_name, plural_name in class_names.items():
                count = storage.count(class_name)
                response[plural_name] = count
            return jsonify(response)
    except Exception as e:
        return jsonify(error=str(e)), 500
