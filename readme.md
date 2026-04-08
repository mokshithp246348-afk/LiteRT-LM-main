# SessionForge: Robust Session Management with Redis

## 🌟 Overview

SessionForge is a sophisticated Python library designed to streamline and secure user session management within your applications. Leveraging the power and speed of Redis, SessionForge provides a robust, scalable, and efficient solution for handling user sessions. Say goodbye to complex session state management and hello to a seamless user experience, powered by blazing-fast caching.

## 🚀 Key Features

*   **Redis-Powered Caching**: Utilizes Redis for high-performance, in-memory session storage, ensuring low latency and high throughput.
*   **Secure Session Creation**: Generates unique, UUID-based session IDs for each new user session.
*   **Effortless Session Retrieval**: Easily fetch session data associated with a given session ID.
*   **Graceful Session Deletion**: Provides a clean mechanism to invalidate and remove user sessions.
*   **Session Expiration**: Automatically handles session timeouts with a default expiry of 24 hours (86400 seconds).
*   **Session Refresh**: Allows for extending the lifespan of an active session.
*   **Environment Variable Configuration**: Flexible setup via `REDIS_CLUSTER_URL` environment variable for Redis connection.

## 🛠️ Installation & Setup

### Prerequisites

*   Python 3.6+
*   Redis Server running and accessible.

### Installation

Install the library using pip:

```bash
pip install redis
```

### Configuration

By default, SessionForge attempts to connect to `redis://localhost:6379/0`. To specify a different Redis instance (e.g., a Redis cluster), set the `REDIS_CLUSTER_URL` environment variable before running your application:

```bash
export REDIS_CLUSTER_URL="redis://your-redis-host:6379/0"
python your_application.py
```

## 💻 Usage Instructions

Here's a basic example of how to use the `SessionManager`:

```python
from session_manager import SessionManager

# Initialize the Session Manager
session_manager = SessionManager()

# User data to be stored in the session
user_info = {"user_id": "user123", "username": "alice"}

# Create a new session
session_id = session_manager.create_session(user_info)
print(f"Session created with ID: {session_id}")

# Retrieve session data
retrieved_data = session_manager.get_session(session_id)
print(f"Retrieved session data: {retrieved_data}")

# Refresh the session (extends expiry)
session_manager.refresh_session(session_id)
print(f"Session {session_id} refreshed.")

# Delete the session
session_manager.delete_session(session_id)
print(f"Session {session_id} deleted.")
```

## 🏗️ Architecture Design

The `SessionManager` class forms the core of this session management layer. It encapsulates all interactions with the Redis cache.

*   **Initialization (`__init__`)**: Establishes a connection to the Redis server, defaulting to `redis://localhost:6379/0` or using the `REDIS_CLUSTER_URL` environment variable. It prints a confirmation message upon successful connection.
*   **Session Creation (`create_session`)**: Generates a unique `uuid4` session ID, serializes the provided `user_data` to JSON, and stores it in Redis with a Time-To-Live (TTL) of 86400 seconds (24 hours). The session ID is returned.
*   **Session Retrieval (`get_session`)**: Retrieves the JSON-serialized session data from Redis using the provided `session_id`. It deserializes the JSON back into a Python dictionary. Returns `None` if the session ID is not found.
*   **Session Deletion (`delete_session`)**: Removes the session data from Redis associated with the given `session_id`. Returns `True` upon successful deletion.
*   **Session Refresh (`refresh_session`)**: Resets the TTL for an existing session to 86400 seconds, effectively extending its validity. Returns `True` upon successful refresh.

The design prioritizes simplicity, efficiency, and scalability by delegating state management to a dedicated, high-performance caching system like Redis.