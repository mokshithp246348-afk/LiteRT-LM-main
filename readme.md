# Redis Rate Limiter

## 🌟 Overview

A robust and efficient rate limiter implemented in Python, leveraging the power of Redis for fast, distributed request throttling. This system is designed to protect your applications from abuse by enforcing limits on the number of requests a user can make within a specified time window. It's perfect for APIs, web services, and any scenario where controlling request volume is critical.

## 🚀 Key Features

*   **Redis-Powered**: Utilizes Redis for high-performance, in-memory storage, enabling sub-millisecond lookups and atomic operations essential for accurate rate limiting.
*   **Distributed by Nature**: Redis's distributed capabilities allow this rate limiter to function seamlessly across multiple application instances, ensuring consistent limits regardless of where a request is processed.
*   **Configurable Limits**: Easily set custom request limits (`limit`) and time windows (`window`) per user to tailor the rate limiting strategy to your specific needs.
*   **Simple API**: A straightforward `is_allowed` method makes integration effortless.
*   **Environment Variable Configuration**: Flexible setup via the `REDIS_CLUSTER_URL` environment variable for specifying your Redis connection.

## 🛠️ Installation & Setup

### Prerequisites

*   **Python 3.6+**: Ensure you have a compatible Python version installed.
*   **Redis Server**: A running Redis instance is required. You can run Redis locally or use a cloud-based service.

### Installation

1.  **Install Dependencies**: This project requires the `redis` Python library.
    ```bash
    pip install redis
    ```

2.  **Configure Redis Connection**: By default, the rate limiter will attempt to connect to `redis://localhost:6379/0`. To use a different Redis instance, set the `REDIS_CLUSTER_URL` environment variable before running your application:
    ```bash
    export REDIS_CLUSTER_URL="redis://your_redis_host:6379/0"
    ```

## 💻 Usage Instructions

### Basic Example

Import the `RateLimiter` class and instantiate it. Then, use the `is_allowed` method to check if a user's request should be permitted.

```python
from rate_limiter import RateLimiter

limiter = RateLimiter()

user_id = "user123"

# Check if the user is allowed to make a request (default: 5 requests per 60 seconds)
if limiter.is_allowed(user_id):
    print(f"Request allowed for {user_id}")
    # Proceed with the request processing...
else:
    print(f"Request denied for {user_id}. Rate limit exceeded.")

# Example with custom limits:
# if limiter.is_allowed(user_id, limit=10, window=300): # 10 requests per 5 minutes
#     print("Request allowed with custom limits.")
# else:
#     print("Request denied with custom limits.")
```

### Understanding `is_allowed` Parameters

*   `user_id` (str): A unique identifier for the user or client making the request.
*   `limit` (int, optional): The maximum number of requests allowed within the specified `window`. Defaults to `5`.
*   `window` (int, optional): The time window in seconds during which the `limit` applies. Defaults to `60` (1 minute).

## 🏗️ Architecture Design

The `RateLimiter` class utilizes a simple yet effective approach based on Redis's key-value store and time-to-live (TTL) functionality. 

1.  **Initialization**: The `RateLimiter` is initialized, establishing a connection to a Redis server. The connection URL can be configured via the `REDIS_CLUSTER_URL` environment variable.
2.  **Request Check (`is_allowed`)**: 
    *   A unique Redis key is generated for each `user_id` (e.g., `rate:<user_id>`).
    *   The current number of requests for the user within the active window is retrieved from Redis using this key.
    *   **First Request**: If the key does not exist (i.e., it's the first request within a new window for this user), the request is allowed. A new key is created in Redis with a value of `1` and an expiration time set to the specified `window`. This automatically handles expiring old counts.
    *   **Subsequent Requests**: If the key exists, its current value (request count) is incremented. If the incremented count is still below the `limit`, the request is allowed. Otherwise, the request is denied.
    *   **Atomicity**: Redis commands like `GET`, `SET EX`, and `INCR` are atomic, ensuring thread-safety and accuracy in a concurrent environment.
3.  **Expiration**: Redis automatically handles the removal of keys after their specified `window` has passed, effectively resetting the rate limit counter for users without manual intervention.