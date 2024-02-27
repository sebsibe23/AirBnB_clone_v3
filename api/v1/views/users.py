#!/usr/bin/python3
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'])
def get_users():
    """
    Retrieves the list of all User objects.
    """
    try:
        users = storage.all(User).values()
        user_list = [user.to_dict() for user in users]
        return jsonify(user_list)
    except Exception:
        abort(500)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a User object based on user_id.
    """
    try:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        return jsonify(user.to_dict())
    except Exception:
        abort(500)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes a User object based on user_id.
    """
    try:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(500)


@app_views.route('/users', methods=['POST'])
def create_user():
    """
    Creates a new User object.
    """
    try:
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        if 'email' not in data:
            abort(400, 'Missing email')
        if 'password' not in data:
            abort(400, 'Missing password')
        user = User(**data)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201
    except Exception:
        abort(500)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates a User object based on user_id.
    """
    try:
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'email', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        storage.save()
        return jsonify(user.to_dict()), 200
    except Exception:
        abort(500)
