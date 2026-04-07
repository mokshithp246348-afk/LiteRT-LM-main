"""
Redis Data Caching Layer
Provides high-performance distributed caching to dramatically reduce database load.

Dependency: requires 'redis' to be installed via pip.
"""
import redis
import os

class MemoryLayer:
    def __init__(self):
        # Requires REDIS_CLUSTER_URL environment variable to be set in production!
        redis_url = os.environ.get("REDIS_CLUSTER_URL", "redis://localhost:6379/0")
        
        self.cache = redis.Redis.from_url(redis_url)
        print("Connected to Distributed Redis Cache...")

    def fetch_fast(self, key):
        return self.cache.get(key)
        
    def write_fast(self, key, value):
        self.cache.set(key, value, ex=3600) # Expire in 1 hour
