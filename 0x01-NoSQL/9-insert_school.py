#!/usr/bin/env python3
"""Module to insert a document in a MongoDB collection."""


def insert_school(mongo_collection, **kwargs):
    """Inserts a document in the collection and returns the new _id."""
    return mongo_collection.insert_one.(kwargs).inserted_id
