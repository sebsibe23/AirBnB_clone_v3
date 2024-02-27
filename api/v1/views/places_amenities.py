#!/usr/bin/python3
from flask import abort, jsonify, request
from models import storage
from api.v1.views import app_views


# Retrieves the list of all Amenity objects of a Place
# GET /api/v1/places/<place_id>/amenities
@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amenities(place_id):
    try:
        place = storage.get("Place", place_id)
        if place is None:
            abort(404)

        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)

    except Exception as e:
        return jsonify(error=str(e)), 500


# Handles adding or deleting an Amenity object to a Place
# POST /api/v1/places/<place_id>/amenities/<amenity_id>
# DELETE /api/v1/places/<place_id>/amenities/<amenity_id>
@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST', 'DELETE'])
def manage_place_amenity(place_id, amenity_id):
    try:
        place = storage.get("Place", place_id)
        amenity = storage.get("Amenity", amenity_id)

        if place is None or amenity is None:
            abort(404)

        if request.method == 'POST':
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200

            place.amenities.append(amenity)
            storage.save()
            return jsonify(amenity.to_dict()), 201

        elif request.method == 'DELETE':
            if amenity not in place.amenities:
                abort(404)

            place.amenities.remove(amenity)
            storage.save()
            return jsonify({}), 200

    except Exception as e:
        return jsonify(error=str(e)), 500
