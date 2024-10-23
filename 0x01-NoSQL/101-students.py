#!/usr/bin/env python3
"""
Module to retrieve top students sorted by average score.
"""

def top_students(mongo_collection):
    """
    Retrieves all students sorted by their average score in descending order.
    
    Args:
        mongo_collection (pymongo.collection.Collection): The MongoDB collection object.
    
    Returns:
        list: A list of dictionaries representing students with an additional key 'averageScore'.
    """
    pipeline = [
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": { "$avg": "$topics.score" }
            }
        },
        {
            "$sort": { "averageScore": -1 }
        }
    ]
    return list(mongo_collection.aggregate(pipeline))

