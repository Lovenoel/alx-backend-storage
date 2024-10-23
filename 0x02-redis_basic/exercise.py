#!/usr/bin/env python3
"""
Redis Cache Module
"""
import redis
import uuid
from typing import Union
from typing import Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """ Decorator to count how many times methods are called """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrap method to increment its call count """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator to store history of inputs and outputs """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Append inputs and outputs to Redis lists """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, output)
        return output

    return wrapper


class Cache:
    """ Cache class for interacting with Redis """

    def __init__(self):
        """ Initialize the Redis client and flush the database """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store data in Redis with a random key and return the key """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis and optionally apply a callable
        to convert it
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """ Retrieve a string from Redis """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """ Retrieve an integer from Redis """
        return self.get(key, int)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store data and count how many times it has been called """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Store data and log history """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def replay(fn: Callable) -> None:
        """ Display the history of calls for a particular function """
        redis_client = redis.Redis()
        func_name = fn.__qualname__
        num_calls = redis_client.get(func_name).decode('utf-8')
        inputs = redis_client.lrange(f"{func_name}:inputs", 0, -1)
        outputs = redis_client.lrange(f"{func_name}:outputs", 0, -1)

        print(f"{func_name} was called {num_calls} times:")

        for inp, outp in zip(inputs, outputs):
            inp_str = inp.decode('utf-8')
            outp_str = outp.decode('utf-8')
            print(f"{func_name}(*{inp_str}) -> {outp_str}")
