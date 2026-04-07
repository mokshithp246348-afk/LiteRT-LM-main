# Redis Cache Service

## 🌟 Overview

This project provides a high-performance, distributed caching layer using Redis. It's designed to dramatically reduce database load by serving frequently accessed data directly from memory. This service is essential for applications requiring rapid data retrieval and high scalability.

## 🚀 Key Features

*   **Distributed Caching:** Leverages Redis to provide a centralized cache accessible across multiple application instances.
*   **Performance Boost:** Significantly speeds up data access by reducing the need for direct database queries.
*   **Database Load Reduction:** Offloads read operations from your primary database, improving its overall performance and stability.
*   **Configurable Expiry:** Cache entries can be set with Time-To-Live (TTL) to ensure data freshness.
*   **Environment Variable Configuration:** Easily configure the Redis connection URL via the `REDIS_CLUSTER_URL` environment variable for production deployments.

## 🛠️ Installation & Setup

1.  **Prerequisites:**
    *   Ensure you have Python installed.
    *   Install the `redis` Python package:
        ```bash
        pip install redis
        ```
    *   A running Redis instance (local or remote).

2.  **Configuration:**
    *   **Development:** The service defaults to connecting to a local Redis instance at `redis://localhost:6379/0`.
    *   **Production:** Set the `REDIS_CLUSTER_URL` environment variable to your Redis cluster's connection string. For example:
        ```bash
        export REDIS_CLUSTER_URL="redis://your-redis-host:6379/0"
        ```

## 💻 Usage Instructions

To utilize the caching layer, instantiate the `MemoryLayer` class and use its `fetch_fast` and `write_fast` methods.

### 1. Initialization:

```python
from redis_cache import MemoryLayer

# Initializes the cache, connecting to Redis
cache_service = MemoryLayer()
```

### 2. Fetching Data:

Use `fetch_fast` to retrieve data associated with a given key.

```python
# Fetch data from cache
cached_data = cache_service.fetch_fast("user:123")

if cached_data:
    print(f"Data found in cache: {cached_data.decode('utf-8')}")
else:
    print("Data not found in cache, fetching from database...")
    # ... fetch data from database ...
    # ... store data in cache using write_fast ...
```

### 3. Writing Data:

Use `write_fast` to store data in the cache. The data will be automatically set to expire after 1 hour (3600 seconds).

```python
# Example: Store user data in cache
user_data = "{"name": "Alice", "email": "alice@example.com"}"
cache_service.write_fast("user:123", user_data)
print("Data written to cache.")
```

## 🏗️ Architecture Design

The `redis_cache.py` module encapsulates the Redis caching logic within the `MemoryLayer` class. This class acts as a facade, simplifying interactions with the underlying `redis-py` library.

*   **`MemoryLayer` Class:**
    *   **`__init__(self)`:** Initializes the connection to Redis. It prioritizes the `REDIS_CLUSTER_URL` environment variable for configuration, falling back to a local default if the variable is not set. This ensures flexibility for different deployment environments.
    *   **`fetch_fast(self, key)`:** Provides a direct interface for retrieving cached values. It takes a cache `key` as input and returns the corresponding `value` from Redis, or `None` if the key does not exist.
    *   **`write_fast(self, key, value)`:** Handles writing data to the cache. It accepts a `key` and `value` pair. Importantly, it sets an expiration time of 1 hour (3600 seconds) for the cache entry to manage cache freshness and prevent stale data.

This design promotes a clean separation of concerns, making the caching mechanism easy to integrate and manage within larger applications.