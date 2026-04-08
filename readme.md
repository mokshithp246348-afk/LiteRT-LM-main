# Redis Cache Layer

## 🌟 Overview

This project provides a high-performance, distributed caching layer using Redis. It's designed to dramatically reduce database load by serving frequently accessed data directly from memory. This ensures rapid data retrieval and significantly improves application responsiveness, especially under heavy traffic conditions.

## 🚀 Key Features

*   **High-Performance Caching:** Leverages Redis for lightning-fast read and write operations.
*   **Distributed Architecture:** Scales horizontally to handle large amounts of data and high request volumes.
*   **Database Load Reduction:** Offloads read-heavy operations from your primary database, improving its performance and stability.
*   **Automatic Expiration:** Implements time-to-live (TTL) for cache entries, ensuring data freshness.
*   **Environment Variable Configuration:** Seamlessly integrates with production environments via `REDIS_CLUSTER_URL`.

## 🛠️ Installation & Setup

**Prerequisites:**

*   Python 3.6+
*   Redis server running locally or accessible via a connection string.

**Installation:**

1.  **Install the Redis Python client:**
    ```bash
    pip install redis
    ```

**Configuration:**

*   **Development:** The cache will default to connecting to `redis://localhost:6379/0`.
*   **Production:** Ensure the `REDIS_CLUSTER_URL` environment variable is set to your Redis cluster's connection string. Example:
    ```bash
    export REDIS_CLUSTER_URL="redis://your-redis-host:6379/0"
    ```

## 💻 Usage Instructions

To utilize the caching layer, instantiate the `MemoryLayer` class. You can then use its methods to fetch data from and write data to the cache.

**Example:**

```python
from redis_cache import MemoryLayer

# Initialize the cache layer
cache = MemoryLayer()

# Write data to the cache (e.g., user profile data)
user_id = "user:123"
user_data = {"name": "Alice", "email": "alice@example.com"}

# Cache the data with an expiration of 1 hour (3600 seconds)
cache.write_fast(user_id, str(user_data)) # Note: Values are typically stored as strings or bytes

# Fetch data from the cache
retrieved_data = cache.fetch_fast(user_id)

if retrieved_data:
    print(f"Data found in cache: {retrieved_data.decode()}") # Decode bytes to string
else:
    print("Data not found in cache. Fetching from database...")
    # ... fetch from database and potentially cache it ...
```

### `MemoryLayer` Methods:

*   `__init__()`:
    Initializes the connection to the Redis cache. Reads `REDIS_CLUSTER_URL` from environment variables or defaults to `redis://localhost:6379/0`.

*   `fetch_fast(key)`:
    Retrieves a value from the cache using the provided `key`. Returns the value if found, otherwise returns `None`.

*   `write_fast(key, value)`:
    Stores a `value` in the cache associated with the given `key`. The entry will expire after 1 hour (3600 seconds).

## 🏗️ Architecture Design

The `Redis Cache Layer` is built around a simple yet powerful client-server architecture:

*   **Client (Your Application):** Integrates with the `MemoryLayer` class to interact with the cache.
*   **`MemoryLayer` Class:** Acts as the interface between your application and the Redis server. It handles establishing the connection and executing cache operations.
*   **Redis Server:** The core caching engine. It stores data in memory for extremely fast access and manages data persistence (if configured) and expiration.

**Connection Management:**

The `MemoryLayer` uses the `redis-py` library to connect to a Redis instance. It prioritizes the `REDIS_CLUSTER_URL` environment variable for configuration, allowing for easy deployment in different environments. The connection is established upon instantiation of the `MemoryLayer` class.

**Data Handling:**

*   **Keys:** Unique identifiers used to store and retrieve data. These are typically strings.
*   **Values:** The data being cached. The `redis-py` library handles serialization/deserialization for basic types, but complex objects should be serialized (e.g., to JSON strings or bytes) before caching.
*   **Expiration:** Cache entries automatically expire after 1 hour (3600 seconds) using the `ex` parameter in the `set` command, preventing stale data from being served indefinitely and managing memory usage.
