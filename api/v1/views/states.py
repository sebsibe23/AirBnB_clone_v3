#!/usr/bin/python3
"""
Defines API actions for State objects.

Routes:
- GET /states: Retrieves list of all State objects.
- GET /states/<state_id>: Retrieves a State object by ID.
- DELETE /states/<state_id>: Deletes a State object by ID.
- POST /states: Creates a new State object.
- PUT /states/<state_id>: Updates a State object by ID.
"""

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


def get_all_states():
    """Retrieves the list of all State objects."""
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states])


def get_state(state_id):
    """Retrieves a State object by its ID."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())


def create_state():
    """Creates a new State object."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


def update_state(state_id):
    """Updates an existing State object."""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    state.update(**data)
    return jsonify(state.to_dict()), 200


def delete_state(state_id):
    """Deletes a State object."""
    try:
        state = storage.get(State, state_id)
        state.delete()
        return jsonify({}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
