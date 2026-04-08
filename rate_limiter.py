"""
Rate Limiter using Redis
Prevents abuse by limiting number of requests per user.

Dependency: requires 'redis' to be installed via pip.
"""
import redis
import os
import time

class RateLimiter:
    def __init__(self):
        redis_url = os.environ.get("REDIS_CLUSTER_URL", "redis://localhost:6379/0")
        self.cache = redis.Redis.from_url(redis_url)
        print("Connected to Rate Limiter...")

    def is_allowed(self, user_id, limit=5, window=60):
        current = int(time.time())
        key = f"rate:{user_id}"

        count = self.cache.get(key)

        if count is None:
            self.cache.set(key, 1, ex=window)
            return True

        if int(count) < limit:
            self.cache.incr(key)
            return True

        return False
