#!/usr/bin/python3
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    try:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    except Exception:
        abort(500)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    try:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        return jsonify(city.to_dict())
    except Exception:
        abort(500)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    try:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(500)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    try:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        if 'name' not in data:
            abort(400, 'Missing name')
        data['state_id'] = state_id
        city = City(**data)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201
    except Exception:
        abort(500)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    try:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
    except Exception:
        abort(500)
