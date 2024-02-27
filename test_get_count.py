#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

# Check if there are any State objects before accessing the first element
if storage.count(State) > 0:
  first_state_id = list(storage.all(State).values())[0].id
  print("First state: {}".format(storage.get(State, first_state_id)))
else:
  print("No State objects found.")
