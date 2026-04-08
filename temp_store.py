"""
Temporary Data Store
Stores short-lived data like OTPs or tokens.

Dependency: requires 'redis' to be installed via pip.
"""
import redis
import os

class TempStore:
    def __init__(self):
        redis_url = os.environ.get("REDIS_CLUSTER_URL", "redis://localhost:6379/0")
        self.cache = redis.Redis.from_url(redis_url)
        print("Connected to Temp Store...")

    def save_temp(self, key, value, expiry=120):
        self.cache.set(key, value, ex=expiry)
        return True

    def get_temp(self, key):
        return self.cache.get(key)

    def delete_temp(self, key):
        self.cache.delete(key)
        return True
