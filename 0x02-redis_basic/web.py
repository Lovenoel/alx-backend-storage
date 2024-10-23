#!/usr/bin/env python3
"""
Web cache and tracker implementation
"""
import redis
import requests
from typing import Callable
from functools import wraps

r = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL and cache the result with expiration.

    Also track how many times the URL has been accessed using Redis.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the page.
    """
    # Track how many times the URL is accessed
    r.incr(f"count:{url}")

    # Check if the page is cached
    cached_page = r.get(f"cached:{url}")
    if cached_page:
        return cached_page.decode('utf-8')

    # If not cached, fetch the page
    response = requests.get(url)
    html_content = response.text

    # Cache the result with an expiration time of 10 seconds
    r.setex(f"cached:{url}", 10, html_content)

    return html_content


def get_url_access_count(url: str) -> int:
    """
    Get the number of times a particular URL was accessed.

    Args:
        url (str): The URL to check access count for.

    Returns:
        int: The number of times the URL was accessed.
    """
    count = r.get(f"count:{url}")
    return int(count) if count else 0


def cache_page(expiration: int = 10) -> Callable:
    """
    Decorator to cache the result of the function and track access count.

    Args:
        expiration (int): The cache expiration time in seconds.

    Returns:
        Callable: The wrapped function with caching and tracking enabled.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str) -> str:
            # Track the URL access count
            r.incr(f"count:{url}")

            # Check if the page is cached
            cached_page = r.get(f"cached:{url}")
            if cached_page:
                return cached_page.decode('utf-8')

            # Fetch the page and cache it with expiration
            result = func(url)
            r.setex(f"cached:{url}", expiration, result)
            return result
        return wrapper
    return decorator


@cache_page(10)
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the page.
    """
    response = requests.get(url)
    return response.text
