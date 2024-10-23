#!/usr/bin/env python3
"""
Inserts a new document in a collection
"""
from pymongo import MongoClient


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs
    Args:
        mongo_collection: pymongo collection object
        **kwargs: key-value pairs for the document fields
    Returns:
        The ID of the inserted document
    """
    return mongo_collection.insert_one.(kwargs).inserted_id
