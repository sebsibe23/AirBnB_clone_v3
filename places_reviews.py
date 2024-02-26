#!/usr/bin/python3
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place.
    """
    try:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    except Exception:
        abort(500)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """
    Retrieves a Review object based on review_id.
    """
    try:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        return jsonify(review.to_dict())
    except Exception:
        abort(500)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Deletes a Review object based on review_id.
    """
    try:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(500)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """
    Creates a new Review object.
    """
    try:
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        if 'user_id' not in data:
            abort(400, 'Missing user_id')
        user = storage.get(User, data['user_id'])
        if user is None:
            abort(404)
        if 'text' not in data:
            abort(400, 'Missing text')
        data['place_id'] = place_id
        review = Review(**data)
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict()), 201
    except Exception:
        abort(500)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Updates a Review object based on review_id.
    """
    try:
        review = storage.get(Review, review_id)
        if review is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)
        storage.save()
        return jsonify(review.to_dict()), 200
    except Exception:
        abort(500)
