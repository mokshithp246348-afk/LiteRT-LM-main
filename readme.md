# Redis Rate Limiter

## 🌟 Overview

This project implements a robust and efficient rate limiting mechanism leveraging Redis. It's designed to protect your applications from abuse by controlling the number of requests a user can make within a specified time window. By using Redis as the backend, it offers high performance and scalability, making it suitable for enterprise-level applications.

## 🚀 Key Features

*   **Redis-Powered**: Utilizes Redis for fast, in-memory storage of request counts and timestamps.
*   **User-Based Limiting**: Allows you to define request limits on a per-user basis.
*   **Configurable Limits**: Easily set the request `limit` and the `window` duration (in seconds).
*   **Environment Variable Configuration**: Supports configuring the Redis connection URL via the `REDIS_CLUSTER_URL` environment variable, defaulting to `redis://localhost:6379/0`.
*   **Simple API**: Provides a straightforward `is_allowed` method to check if a request should be permitted.

## 🛠️ Installation & Setup

**Dependencies**: This project requires the `redis` Python library. Install it using pip:

```bash
pip install redis
```

**Redis Setup**: Ensure you have a Redis instance running. You can connect to a local instance by default or specify a different Redis cluster URL using the `REDIS_CLUSTER_URL` environment variable.

## 💻 Usage Instructions

1.  **Instantiate the RateLimiter**:

    ```python
    from rate_limiter import RateLimiter

    limiter = RateLimiter()
    ```

2.  **Check if a request is allowed**:

    Use the `is_allowed` method, passing a unique `user_id` and optionally customizing the `limit` and `window`.

    ```python
    user_id = "user123"

    if limiter.is_allowed(user_id):
        print(f"Request for {user_id} is allowed.")
        # Proceed with the request...
    else:
        print(f"Rate limit exceeded for {user_id}. Please try again later.")
        # Reject the request or return an appropriate response.
    ```

    **Example with custom limits**:

    ```python
    # Allow 10 requests per user every 30 seconds
    if limiter.is_allowed(user_id, limit=10, window=30):
        # ...
    else:
        # ...
    ```

## 🏗️ Architecture Design

The `RateLimiter` class is the core component of this system. It utilizes the `redis-py` library to interact with a Redis instance. 

*   **Initialization**: The `__init__` method establishes a connection to Redis. It attempts to use the `REDIS_CLUSTER_URL` environment variable for configuration; if not found, it defaults to a local Redis instance running on `localhost:6379`.
*   **Request Checking (`is_allowed`)**: This method is the primary interface for rate limiting. 
    *   It constructs a unique Redis key based on the `user_id` (e.g., `rate:user123`).
    *   It checks the current request count for the user in Redis. 
    *   If no record exists (first request within the window), it sets the key with an expiration time equal to the `window` and returns `True`.
    *   If a record exists and the count is below the `limit`, it increments the count and returns `True`.
    *   If the count has reached or exceeded the `limit`, it returns `False`, indicating that the request should be denied.
*   **Redis Integration**: Redis is used for its atomic operations (like `INCR`) and its built-in expiration mechanism (`EXPIRE` or `SET EX`), which automatically handles the resetting of limits after the defined `window` has passed. This ensures efficiency and accurate rate limiting without manual cleanup.