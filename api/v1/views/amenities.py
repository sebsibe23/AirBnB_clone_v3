#!/usr/bin/python3
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """
    Retrieves the list of all Amenity objects.
    """
    try:
        amenities = storage.all(Amenity).values()
        amenity_list = [amenity.to_dict() for amenity in amenities]
        return jsonify(amenity_list)
    except Exception:
        abort(500)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """
    Retrieves a Amenity object based on amenity_id.
    """
    try:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        return jsonify(amenity.to_dict())
    except Exception:
        abort(500)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes a Amenity object based on amenity_id.
    """
    try:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(500)


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """
    Creates a new Amenity object.
    """
    try:
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        if 'name' not in data:
            abort(400, 'Missing name')
        amenity = Amenity(**data)
        storage.new(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
    except Exception:
        abort(500)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates a Amenity object based on amenity_id.
    """
    try:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
    except Exception:
        abort(500)
