#!/usr/bin/python3
'''
View for Amenity objects that handles all default RESTFul API actions
'''
from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def get_and_post_amenity():
    '''
    Handles GET and POST actions for amenities
    '''
    try:
        if request.method == 'GET':
            amenity_obj = storage.all(Amenity)
            if amenity_obj is None:
                abort(404)
            amenity_list = []
            for value in amenity_obj.values():
                amenity_list.append(value.to_dict())
            return jsonify(amenity_list)

        if request.method == 'POST':
            content_type = request.headers.get('Content-Type')
            if content_type == 'application/json':
                body = request.get_json()
                if 'name' in body:
                    new_amenity = Amenity(**body)
                    storage.new(new_amenity)
                    storage.save()
                    return make_response(jsonify(new_amenity.to_dict()), 201)
                else:
                    abort(400, description='Missing name')
            else:
                abort(400, description='Not a JSON')
    except Exception as e:
        return jsonify(error=str(e)), 500


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_del_post_amenity(amenity_id):
    '''
    Handles GET, DELETE, and PUT actions with provided amenity_id
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
            if content_type == 'application/json':
                body = request.get_json()
                banned_keys = ['id', 'created_at', 'updated_at']
                for key, value in body.items():
                    if key not in banned_keys:
                        setattr(amenity_obj, key, value)
                storage.save()
                return make_response(jsonify(amenity_obj.to_dict()), 200)
            else:
                abort(400, description='Not a JSON')
    except Exception as e:
        return jsonify(error=str(e)), 500
