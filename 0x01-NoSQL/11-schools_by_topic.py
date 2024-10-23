#!/usr/bin/env python3
"""
Finds schools that offer a specific topic
"""
from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of schools having a specific topic
    Args:
        mongo_collection: pymongo collection object
        topic (str): topic to search for
    """
    return list(mongo_collection.find({"topics": topic}))
