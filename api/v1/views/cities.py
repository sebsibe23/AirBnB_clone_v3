#!/usr/bin/python3

'''
Flask view for `City` objects within a `State` object
Handles GET, POST, PUT, DELETE requests
'''

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def state_by_city(state_id):
    '''
    GET: Retrieves all cities of a state by state ID.
    POST: Creates a new city for a specific state.

    Raises:
        400: Bad request (missing name or invalid content type).
        404: Not found (state or city not found).
    '''
    try:
        if request.method == 'GET':
            state_obj = storage.get(State, state_id)
            cities = []
            if state_obj is None:
                abort(404)
            city_obj = getattr(state_obj, 'cities')
            for city in city_obj:
                cities.append(city.to_dict())
            return jsonify(cities)

        if request.method == 'POST':
            state_obj = storage.get(State, state_id)
            if state_obj is None:
                abort(404)
            content_type = request.headers.get('Content-Type')
            if content_type != 'application/json':
                abort(400, description='Not a JSON')

            body = request.get_json()
            if 'name' not in body:
                abort(400, description='Missing name')

            new_city = City(**body)
            setattr(new_city, 'state_id', state_id)
            storage.new(new_city)
            storage.save()
            return make_response(jsonify(new_city.to_dict()), 201)
    except Exception as e:
        abort(400, description=str(e))


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def city_by_city(city_id):
    '''
    GET: Retrieves a city by city ID.
    PUT: Updates a city by city ID.
    DELETE: Deletes a city by city ID.

    Raises:
        400: Bad request (invalid content type).
        404: Not found (city not found).
    '''
    try:
        if request.method == 'GET':
            city_obj = storage.get(City, city_id)
            if city_obj is None:
                abort(404)
            return jsonify(city_obj.to_dict())

        if request.method == 'DELETE':
            city_obj = storage.get(City, city_id)
            if city_obj is None:
                abort(404)
            storage.delete(city_obj)
            storage.save()
            return make_response({}, 200)

        if request.method == 'PUT':
            city_obj = storage.get(City, city_id)
            if city_obj is None:
                abort(404)
            content_type = request.headers.get('Content-Type')
            if content_type != 'application/json':
                abort(400, description='Not a JSON')

            body = request.get_json()
            banned_keys = ['id', 'state_id', 'created_at', 'updated_at']
            for key, value in body.items():
                if key not in banned_keys:
                    setattr(city_obj, key, value)
            storage.save()
            return make_response(jsonify(city_obj.to_dict()), 200)
    except Exception as e:
        abort(400, description=str(e))
