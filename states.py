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


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves list of all State objects."""
    try:
        states = storage.all(State).values()
        states_list = [state.to_dict() for state in states]
        return jsonify(states_list)
    except Exception as e:
        abort(500, str(e))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object by ID."""
    try:
        state = storage.get(State, state_id)
        if state is None:
            abort(404, 'State not found')
        return jsonify(state.to_dict())
    except Exception as e:
        abort(500, str(e))


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object by ID."""
    try:
        state = storage.get(State, state_id)
        if state is None:
            abort(404, 'State not found')
        storage.delete(state)
        storage.save()
        return jsonify({})
    except Exception as e:
        abort(500, str(e))


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new State object."""
    try:
        if not request.is_json:
            abort(400, 'Invalid JSON')
        data = request.get_json()
        if 'name' not in data:
            abort(400, 'Missing name')
        state = State(**data)
        storage.new(state)
        storage.save()
        return jsonify(state.to_dict()), 201
    except Exception as e:
        abort(500, str(e))


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by ID."""
    try:
        state = storage.get(State, state_id)
        if state is None:
            abort(404, 'State not found')
        if not request.is_json:
            abort(400, 'Invalid JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict())
    except Exception as e:
        abort(500, str(e))
