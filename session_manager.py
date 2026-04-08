"""
Session Management Layer
Handles user session storage using Redis cache.

Dependency: requires 'redis' to be installed via pip.
"""
import redis
import os
import json
import uuid

class SessionManager:
    def __init__(self):
        redis_url = os.environ.get("REDIS_CLUSTER_URL", "redis://localhost:6379/0")
        self.cache = redis.Redis.from_url(redis_url)
        print("Connected to Redis for Session Management...")

    def create_session(self, user_data):
        session_id = str(uuid.uuid4())
        self.cache.set(session_id, json.dumps(user_data), ex=86400)
        return session_id

    def get_session(self, session_id):
        data = self.cache.get(session_id)
        return json.loads(data) if data else None

    def delete_session(self, session_id):
        self.cache.delete(session_id)
        return True

    def refresh_session(self, session_id):
        self.cache.expire(session_id, 86400)
        return True
