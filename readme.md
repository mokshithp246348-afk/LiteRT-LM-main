# Redis Rate Limiter

## 🌟 Overview

This project implements a robust rate limiting mechanism powered by Redis. It's designed to protect your applications from abuse by controlling the number of requests a user can make within a specified time window. By leveraging Redis, this rate limiter offers high performance and scalability, ensuring your services remain available and responsive.

## 🚀 Key Features

*   **Redis-Powered**: Utilizes Redis for fast, in-memory storage of request counts and expiry.
*   **Configurable Limits**: Easily set the request limit and the time window for each user.
*   **User-Specific Tracking**: Tracks request rates independently for each unique user ID.
*   **Simple API**: Provides a straightforward interface to check if a request is allowed.
*   **Environment Variable Configuration**: Supports custom Redis connection URLs via the `REDIS_CLUSTER_URL` environment variable.

## 🛠️ Installation & Setup

### Prerequisites

*   Python 3.7+
*   Redis server running and accessible

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Install Dependencies**:
    This project requires the `redis` Python library.
    ```bash
    pip install redis
    ```

3.  **Configure Redis Connection (Optional)**:
    By default, the rate limiter connects to `redis://localhost:6379/0`. If your Redis instance is elsewhere, set the `REDIS_CLUSTER_URL` environment variable:
    ```bash
    export REDIS_CLUSTER_URL="redis://your-redis-host:6379/0"
    ```

## 💻 Usage Instructions

To use the rate limiter, instantiate the `RateLimiter` class and then call the `is_allowed` method for each incoming request.

### Basic Example

```python
from rate_limiter import RateLimiter

limiter = RateLimiter()

user_id = "user123"

if limiter.is_allowed(user_id):
    print("Request allowed!")
    # Process the request...
else:
    print("Rate limit exceeded. Please try again later.")
```

### Custom Limits and Window

You can specify custom `limit` and `window` (in seconds) for the rate limiter:

```python
from rate_limiter import RateLimiter

limiter = RateLimiter()

user_id = "user456"
request_limit = 10  # Allow 10 requests
window_seconds = 300  # Within a 5-minute window

if limiter.is_allowed(user_id, limit=request_limit, window=window_seconds):
    print("Request allowed!")
    # Process the request...
else:
    print("Rate limit exceeded. Please try again later.")
```

## 🏗️ Architecture Design

The `RateLimiter` class forms the core of this system. It relies on Redis to maintain the state of request counts for each user.

*   **`__init__(self)`**: Initializes the connection to Redis. It attempts to use the `REDIS_CLUSTER_URL` environment variable for the Redis endpoint; otherwise, it defaults to `redis://localhost:6379/0`.
*   **`is_allowed(self, user_id, limit=5, window=60)`**: This method is the primary interface for checking rate limits. 
    *   It constructs a unique Redis key for the given `user_id` (e.g., `rate:user123`).
    *   It checks the current request count for the user in Redis.
    *   If no record exists for the user, it sets the count to 1 with an expiration time equal to the `window` and returns `True`.
    *   If a record exists and the current count is less than the `limit`, it increments the count and returns `True`.
    *   If the count has reached or exceeded the `limit`, it returns `False`.

The use of Redis's atomic `INCR` and `SET` with expiration (`EX`) ensures thread-safety and efficient handling of concurrent requests.