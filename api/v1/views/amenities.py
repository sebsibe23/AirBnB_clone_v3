#!/usr/bin/python3

'''
Flask view for `Amenity` objects
Handles GET, POST, DELETE, PUT requests
'''

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_and_post_amenity():
    '''
    GET: Retrieves all amenities.
    POST: Creates a new amenity.

    Raises:
        400: Bad request (missing name or invalid content type).
        404: Not found (amenity not found).
    '''
    try:
        if request.method == 'GET':
            amenity_obj = storage.all(Amenity)
            if amenity_obj is None:
                abort(404)
            amenity_list = [value.to_dict() for value in amenity_obj.values()]
            return jsonify(amenity_list)

        if request.method == 'POST':
            content_type = request.headers.get('Content-Type')
            if content_type != 'application/json':
                abort(400, description='Not a JSON')

            body = request.get_json()
            if 'name' not in body:
                abort(400, description='Missing name')

            new_amenity = Amenity(**body)
            storage.new(new_amenity)
            storage.save()
            return make_response(jsonify(new_amenity.to_dict()), 201)
    except Exception as e:
        abort(400, description=str(e))


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_del_post_amenity(amenity_id):
    '''
    GET: Retrieves an amenity by ID.
    DELETE: Deletes an amenity by ID.
    PUT: Updates an amenity by ID.

    Raises:
        400: Bad request (invalid content type).
        404: Not found (amenity not found).
    '''
    try:
        if request.method == 'GET':
            amenity_obj = storage.get(Amenity, amenity_id)
            if amenity_obj is None:
                abort(404)
            return jsonify(amenity_obj.to_dict())

        if request.method == 'DELETE':
            amenity_obj = storage.get(Amenity, amenity_id)
            if amenity_obj is None:
                abort(404)
            storage.delete(amenity_obj)
            storage.save()
            return make_response({}, 200)

        if request.method == 'PUT':
            amenity_obj = storage.get(Amenity, amenity_id)
            if amenity_obj is None:
                abort(404)
            content_type = request.headers.get('Content-Type')
            if content_type != 'application/json':
                abort(400, description='Not a JSON')

            body = request.get_json()
            banned_keys = ['id', 'created_at', 'updated_at']
            for key, value in body.items():
                if key not in banned_keys:
                    setattr(amenity_obj, key, value)
            storage.save()
            return make_response(jsonify(amenity_obj.to_dict()), 200)
    except Exception as e:
        abort(400, description=str(e))
