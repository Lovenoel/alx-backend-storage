#!/usr/bin/env python3
"""
Module to provide statistics about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def log_stats():
    """
    Prints statistics about Nginx logs.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    nginx_collection = db.nginx

    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    status_count = nginx_collection.count_documents({"path": "/status"})
    print(f"{status_count} status check")

    # Aggregation pipeline to find top 10 IPs
    pipeline = [
        {
            "$group": {
                "_id": "$ip",
                "count": { "$sum": 1 }
            }
        },
        {
            "$sort": { "count": -1 }
        },
        {
            "$limit": 10
        }
    ]

    top_ips = nginx_collection.aggregate(pipeline)
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip.get('_id')}: {ip.get('count')}")
