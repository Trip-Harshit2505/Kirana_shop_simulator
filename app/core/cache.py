import time

# Simple in-memory cache implementation

# This cache is used to store results of expensive operations like finding the nearest warehouse or calculating shipping charges. It uses a dictionary to store values along with their expiry time. The `get` method checks if the key exists and if it has not expired before returning the value. The `set` method allows storing a value with an optional time-to-live (TTL) after which the value will be considered expired and removed from the cache. This helps improve performance by avoiding redundant calculations for frequently accessed data.

class SimpleCache:
    def __init__(self):
        self.store = {}

    def get(self, key):
        if key in self.store:
            value, expiry = self.store[key]
            if expiry is None or expiry > time.time():
                return value
            else:
                del self.store[key]
        return None

    def set(self, key, value, ttl=None):
        expiry = time.time() + ttl if ttl else None
        self.store[key] = (value, expiry)


cache = SimpleCache()