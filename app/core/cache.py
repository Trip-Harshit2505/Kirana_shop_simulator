import time


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