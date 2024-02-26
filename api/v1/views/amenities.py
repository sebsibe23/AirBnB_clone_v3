#!/usr/bin/python3
"""
Flask route that returns JSON response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from


@app_views.route('/amenities/', methods=['GET', 'POST'])
@swag_from('swagger_yaml/amenities_no_id.yml', methods=['GET', 'POST'])
def amenities_no_id(amenity_id=None):
    """
    Amenities route that handles HTTP requests when no ID is given.

    Parameters:
    - amenity_id: (str) Optional ID of the amenity.

    Returns:
    - JSON response: List of all amenities in case of GET request.
                     New amenity object in case of POST request.

    Raises:
    - 400 (Bad Request): If request does not contain valid JSON or is missing name.
    """
    try:
        if request.method == 'GET':
            all_amenities = storage.all('Amenity')
            all_amenities = [obj.to_json() for obj in all_amenities.values()]
            return jsonify(all_amenities)

        if request.method == 'POST':
            req_json = request.get_json()
            if req_json is None:
                abort(400, 'Not a JSON')
            if req_json.get('name') is None:
                abort(400, 'Missing name')
            Amenity = CNC.get('Amenity')
            new_object = Amenity(**req_json)
            new_object.save()
            return jsonify(new_object.to_json()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/amenities_id.yml', methods=['GET', 'DELETE', 'PUT'])
def amenities_with_id(amenity_id=None):
    """
    Amenities route that handles HTTP requests when an ID is given.

    Parameters:
    - amenity_id: (str) ID of the amenity.

    Returns:
    - JSON response: Amenity object in case of GET request.
                     Empty response in case of DELETE request.
                     Updated amenity object in case of PUT request.

    Raises:
    - 400 (Bad Request): If request does not contain valid JSON.
    - 404 (Not Found): If amenity with the given ID does not exist.
    """
    try:
        amenity_obj = storage.get('Amenity', amenity_id)
        if amenity_obj is None:
            abort(404, 'Not found')

        if request.method == 'GET':
            return jsonify(amenity_obj.to_json())

        if request.method == 'DELETE':
            amenity_obj.delete()
            del amenity_obj
            return jsonify({}), 200

        if request.method == 'PUT':
            req_json = request.get_json()
            if req_json is None:
                abort(400, 'Not a JSON')
            amenity_obj.bm_update(req_json)
            return jsonify(amenity_obj.to_json()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
