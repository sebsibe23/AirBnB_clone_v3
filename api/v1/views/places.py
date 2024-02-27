#!/usr/bin/python3
""" objects that handle
default RestFul API actions for Places """
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def city_places(city_id):
    """
    Handles all default RESTFul API actions for Place objects within a City.

    Args:
        city_id (str): ID of the City object.

    Returns:
        JSON: A dictionary representing the response.
    """

    city = storage.get(City, city_id)
    if city is None:
        abort(404, description="City not found")

    if request.method == 'GET':
        place_list = [place.to_dict() for place in city.places]
        return jsonify(place_list)

    if request.method == 'POST':
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            abort(400, description="Not a JSON")
        place_dict = request.get_json()
        if 'user_id' not in place_dict:
            abort(400, description="Missing user_id")
        user = storage.get(User, place_dict['user_id'])
        if user is None:
            abort(404, description="User not found")
        if 'name' not in place_dict:
            abort(400, description="Missing name")
        place_dict['city_id'] = city_id
        new_place = Place(**place_dict)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201

    return abort(405, description="Method not allowed")


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place(place_id):
    """
    Handles all default RESTFul API actions for Place objects.

    Args:
        place_id (str): ID of the Place object.

    Returns:
        JSON: A dictionary representing the response.
    """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            abort(400, description="Not a JSON")
        place_dict = request.get_json()
        ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in place_dict.items():
            if key not in ignored_keys:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200

    return abort(405, description="Method not allowed")

