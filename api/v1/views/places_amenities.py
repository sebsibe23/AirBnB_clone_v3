#!/usr/bin/python3
from flask import jsonify, abort, request
from models import storage, Place, Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET', 'POST', 'DELETE'], strict_slashes=False)
def place_amenities(place_id):
    """
    Handles all default RESTFul API actions for
    Place-Amenity relationships.

    Args:
        place_id (str): ID of the Place object.

    Returns:
        JSON: A dictionary representing the response.
    """

    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")

    if request.method == 'GET':
        amenity_ids = place.amenity_ids
        amenities = [
           storage.get(Amenity, amenity_id) for amenity_id in amenity_ids
        ]
        amenity_list = [amenity.to_dict() for amenity in amenities]
        return jsonify(amenity_list)

    elif request.method == 'POST':
        amenity_id = request.path.split('/')[-1]
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404, description="Amenity not found")
        if amenity.id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity.id)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    elif request.method == 'DELETE':
        amenity_id = request.path.split('/')[-1]
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404, description="Amenity not found")
        if amenity.id not in place.amenity_ids:
            abort(404, description="Amenity not linked to the Place")
        place.amenity_ids.remove(amenity.id)
        storage.save()
        return jsonify({}), 200

    return abort(405, description="Method not allowed")
