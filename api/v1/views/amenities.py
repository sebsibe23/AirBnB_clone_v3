#!/usr/bin/python3
from flask import Flask, jsonify, abort, request
from models.amenity import Amenity
from api.v1.views import app_views

app = Flask(__name__)


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """
    Retrieves a list of all amenities.

    Returns:
        jsonify: JSON response containing the list of amenities.
    """
    try:
        amenities = [amenity.to_dict() for amenity in Amenity.query.all()]
        return jsonify(amenities)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """
    Retrieves a specific amenity by its ID.

    Args:
        amenity_id (str): The ID of the amenity.

    Returns:
        jsonify: JSON response containing the amenity details.
    """
    try:
        amenity = Amenity.query.get(amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes a specific amenity by its ID.

    Args:
        amenity_id (str): The ID of the amenity.

    Returns:
        jsonify: Empty JSON response with a 200 status code.
    """
    try:
        amenity = Amenity.query.get(amenity_id)
        if amenity is None:
            abort(404)
        amenity.delete()
        return jsonify({}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """
    Creates a new amenity.

    Returns:
        jsonify: JSON response containing the newly created amenity.
    """
    try:
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        if 'name' not in data:
            abort(400, 'Missing name')
        amenity = Amenity(**data)
        amenity.save()
        return jsonify(amenity.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates an existing amenity by its ID.

    Args:
        amenity_id (str): The ID of the amenity.

    Returns:
        jsonify: JSON response containing the updated amenity.
    """
    try:
        amenity = Amenity.query.get(amenity_id)
        if amenity is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
