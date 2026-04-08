# Redis Rate Limiter

## 🌟 Overview

This project provides a robust and efficient rate-limiting solution leveraging Redis. It's designed to protect your applications from abuse by controlling the number of requests a user can make within a specified time window. This implementation is perfect for APIs, web services, or any application where controlling request frequency is crucial for stability, performance, and security.

## 🚀 Key Features

*   **Redis-Powered:** Utilizes Redis for fast, in-memory storage of request counts and expiration times, ensuring high performance.
*   **User-Centric Limiting:** Easily track and limit requests on a per-user basis using unique `user_id`s.
*   **Configurable Limits:** Define custom request limits (`limit`) and time windows (`window`) to suit your application's specific needs.
*   **Environment Variable Configuration:** Supports flexible Redis connection configuration via the `REDIS_CLUSTER_URL` environment variable, defaulting to `redis://localhost:6379/0`.
*   **Simple Integration:** Designed for straightforward integration into existing Python applications.

## 🛠️ Installation & Setup

**Prerequisites:**

*   Python 3.6+
*   A running Redis instance (local or remote).

**Installation:**

1.  **Install the Redis Python client:**
    ```bash
    pip install redis
    ```

2.  **Configure Redis Connection (Optional):**
    Set the `REDIS_CLUSTER_URL` environment variable to point to your Redis instance. If not set, it defaults to `redis://localhost:6379/0`.
    ```bash
    export REDIS_CLUSTER_URL="redis://your_redis_host:6379/0"
    ```

## 💻 Usage Instructions

Integrate the `RateLimiter` class into your application logic to enforce request limits.

**Example:**

```python
from rate_limiter import RateLimiter

limiter = RateLimiter()

user_id = "user123"

# Check if the request is allowed (default limit of 5 requests per 60 seconds)
if limiter.is_allowed(user_id):
    print(f"Request from {user_id} is allowed.")
    # Process the request...
else:
    print(f"Request from {user_id} denied. Rate limit exceeded.")
    # Return a 429 Too Many Requests error

# Example with custom limits
if limiter.is_allowed(user_id, limit=10, window=300): # 10 requests per 5 minutes
    print(f"Custom limit request from {user_id} is allowed.")
else:
    print(f"Custom limit request from {user_id} denied.")
```

## 🏗️ Architecture Design

The `RateLimiter` class employs a simple yet effective algorithm using Redis for tracking request counts:

1.  **Initialization (`__init__`)**: 
    *   Establishes a connection to the Redis server using the `redis-py` library. 
    *   It attempts to read the `REDIS_CLUSTER_URL` environment variable for configuration, falling back to a local Redis instance if the variable is not set.
    *   A confirmation message is printed upon successful connection.

2.  **Request Allowance Check (`is_allowed`)**: 
    *   Takes a `user_id`, an optional `limit` (defaulting to 5), and an optional `window` in seconds (defaulting to 60) as parameters.
    *   Generates a unique Redis key for the user (e.g., `rate:user123`).
    *   Retrieves the current request count for the user from Redis.
    *   **If no record exists (first request in window):** 
        *   Sets the key in Redis with a value of `1` and an expiration time equal to the `window`. This establishes the initial count and the time frame.
        *   Returns `True` (request allowed).
    *   **If a record exists:** 
        *   Checks if the current count is less than the specified `limit`.
        *   If the count is below the limit, increments the count using `INCR` and returns `True` (request allowed).
        *   If the count has reached or exceeded the limit, returns `False` (request denied).

This design ensures that request counts are automatically reset after the specified `window` due to Redis's `EX` (expiration) option, making it a stateless and scalable rate-limiting solution.
