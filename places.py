#!/usr/bin/python3
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City.
    """
    try:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    except Exception:
        abort(500)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Retrieves a Place object based on place_id.
    """
    try:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        return jsonify(place.to_dict())
    except Exception:
        abort(500)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place object based on place_id.
    """
    try:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(500)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    Creates a new Place object.
    """
    try:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)
        if 'name' not in data:
            abort(400, 'Missing name')
        data['city_id'] = city_id
        place = Place(**data)
        storage.new(place)
        storage.save()
        return jsonify(place.to_dict()), 201
    except Exception:
        abort(500)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Updates a Place object based on place_id.
    """
    try:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        storage.save()
        return jsonify(place.to_dict()), 200
    except Exception:
        abort(500)

# new code 

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects based on the JSON body of the request
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify([place.to_dict() for place in storage.all(Place).values()])

        states = data.get('states', [])
        cities = data.get('cities', [])
        amenities = data.get('amenities', [])

        if not isinstance(states, list) or not isinstance(cities, list) or not isinstance(amenities, list):
            abort(400, 'Not a JSON')

        if not states and not cities and not amenities:
            return jsonify([place.to_dict() for place in storage.all(Place).values()])

        places = []
        for state_id in states:
            state = storage.get(State, state_id)
            if state is not None:
                for city in state.cities:
                    if city.id not in cities:
                        cities.append(city.id)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city is not None:
                for place in city.places:
                    if all(amenity_id in place.amenity_ids for amenity_id in amenities):
                        places.append(place)

        return jsonify([place.to_dict() for place in places])

    except Exception:
        abort(400, 'Not a JSON')
