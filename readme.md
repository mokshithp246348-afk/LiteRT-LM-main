# Redis Cache Layer

## 🌟 Overview

This project introduces a high-performance, distributed caching layer using Redis. It's designed to dramatically reduce the load on your primary database by serving frequently accessed data directly from the cache. This ensures faster response times and a more scalable application architecture.

## 🚀 Key Features

*   **High-Performance Caching:** Leverages Redis for lightning-fast data retrieval and storage.
*   **Distributed Architecture:** Scales horizontally to handle increasing loads.
*   **Reduced Database Load:** Offloads read operations from your main database, improving overall performance and availability.
*   **Easy Integration:** Simple class-based API for seamless integration into existing applications.
*   **Configurable Expiration:** Data can be set with Time-To-Live (TTL) to ensure freshness.

## 🛠️ Installation & Setup

1.  **Install Redis:** Ensure you have a Redis server running. For local development, you can use Docker:
    ```bash
    docker run --name redis-stack -d -p 6379:6379 redis/redis-stack:latest
    ```

2.  **Install Python Redis Client:**
    ```bash
    pip install redis
    ```

3.  **Environment Variable:** For production environments, set the `REDIS_CLUSTER_URL` environment variable to point to your Redis cluster. If not set, it defaults to `redis://localhost:6379/0`.

    *   **Example (Linux/macOS):**
        ```bash
        export REDIS_CLUSTER_URL="redis://your-redis-host:6379/0"
        ```
    *   **Example (Windows CMD):**
        ```cmd
        set REDIS_CLUSTER_URL=redis://your-redis-host:6379/0
        ```
    *   **Example (Windows PowerShell):**
        ```powershell
        $env:REDIS_CLUSTER_URL="redis://your-redis-host:6379/0"
        ```

## 💻 Usage Instructions

Instantiate the `MemoryLayer` class and use its methods to interact with the cache.

```python
from redis_cache import MemoryLayer

# Initialize the cache layer
cache = MemoryLayer()

# Write data to the cache (value will expire in 1 hour)
cache.write_fast("user:123", "{'name': 'Alice', 'email': 'alice@example.com'}")

# Fetch data from the cache
user_data = cache.fetch_fast("user:123")

if user_data:
    print(f"Data found in cache: {user_data}")
else:
    print("Data not found in cache.")

# Example of fetching non-existent key
non_existent_data = cache.fetch_fast("non_existent_key")
if not non_existent_data:
    print("Successfully confirmed non-existent key returns None.")
```

## 🏗️ Architecture Design

The `MemoryLayer` class is the core component, providing a simple interface to a distributed Redis cache.

*   **`__init__(self)`:**
    *   Initializes the connection to Redis.
    *   Reads the `REDIS_CLUSTER_URL` from environment variables, defaulting to a local Redis instance (`redis://localhost:6379/0`).
    *   Establishes a connection using the `redis-py` library.
    *   Prints a confirmation message upon successful connection.

*   **`fetch_fast(self, key)`:**
    *   Retrieves a value from Redis given a specific `key`.
    *   Returns the value if found, otherwise returns `None`.

*   **`write_fast(self, key, value)`:**
    *   Stores a `value` in Redis associated with a `key`.
    *   Sets an expiration time of 1 hour (3600 seconds) for the cache entry.

This design prioritizes speed and simplicity, making it straightforward to implement caching in various parts of an application.