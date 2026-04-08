# Redis Rate Limiter

## 🌟 Overview

This project implements a robust rate limiting mechanism leveraging Redis. It's designed to protect your applications from abuse by controlling the number of requests a user can make within a specified time window. By utilizing Redis, we ensure high performance and scalability for your rate limiting needs.

## 🚀 Key Features

*   **Redis-Powered**: Leverages Redis for fast, in-memory storage of request counts.
*   **Configurable Limits**: Easily set the maximum number of requests allowed (`limit`) and the time window duration (`window`) in seconds.
*   **User-Specific Limiting**: Tracks request counts on a per-user basis using `user_id`.
*   **Automatic Expiration**: Redis keys automatically expire after the specified `window`, resetting the count for users.
*   **Environment Variable Configuration**: Supports configuring the Redis connection URL via the `REDIS_CLUSTER_URL` environment variable, defaulting to `redis://localhost:6379/0`.

## 🛠️ Installation & Setup

**Prerequisites**: 
*   Python 3.x installed on your system.
*   A running Redis instance.

**Installation**: 
1.  Clone this repository:
    ```bash
    git clone <your-repository-url>
    cd <your-repository-directory>
    ```
2.  Install the required Python package:
    ```bash
    pip install redis
    ```

**Redis Configuration**: 
Ensure your Redis server is accessible. You can configure the connection URL by setting the `REDIS_CLUSTER_URL` environment variable. For example:

```bash
export REDIS_CLUSTER_URL="redis://your_redis_host:6379/0"
```

If not set, the application will default to connecting to Redis on `localhost:6379`.

## 💻 Usage Instructions

To use the rate limiter, instantiate the `RateLimiter` class and then call the `is_allowed` method.

```python
from rate_limiter import RateLimiter

# Initialize the rate limiter
limiter = RateLimiter()

# Example usage for a user
user_id = "user123"

# Check if the request is allowed (default limit of 5 requests per 60 seconds)
if limiter.is_allowed(user_id):
    print(f"Request from {user_id} is allowed.")
    # Process the request...
else:
    print(f"Request from {user_id} is denied. Rate limit exceeded.")

# Example with custom limits
if limiter.is_allowed(user_id, limit=10, window=120):
    print(f"Request from {user_id} is allowed with custom limits.")
else:
    print(f"Request from {user_id} is denied with custom limits.")
```

## 🏗️ Architecture Design

The `RateLimiter` class is the core component of this system. It establishes a connection to a Redis instance upon initialization.

*   **`__init__(self)`**: This constructor initializes the connection to Redis. It reads the `REDIS_CLUSTER_URL` from environment variables or defaults to a local Redis instance. A confirmation message is printed to the console upon successful connection.
*   **`is_allowed(self, user_id, limit=5, window=60)`**: This method checks if a request from a given `user_id` should be permitted based on the defined `limit` and `window`. 
    *   It constructs a unique Redis key using the `user_id`. 
    *   It retrieves the current request count from Redis for that `user_id`.
    *   If no record exists, it creates a new entry with a count of 1 and sets an expiration time (`ex=window`), returning `True`.
    *   If a record exists and the count is below the `limit`, it increments the count and returns `True`.
    *   If the count has reached or exceeded the `limit`, it returns `False`.

The design relies on Redis's atomic operations (`INCR`, `SET` with `EX`) to ensure thread-safety and accuracy in count management.