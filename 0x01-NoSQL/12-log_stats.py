#!/usr/bin/env python3
"""
Script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient

def log_stats():
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs  # Use the logs database
    nginx_collection = db.nginx  # Use the nginx collection

    # Count total logs
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    # Prepare HTTP method counts
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")

    # Count logs for each method
    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    # Count for specific GET method and path
    status_check_count = nginx_collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status_check_count} status check")

if __name__ == "__main__":
    log_stats()
