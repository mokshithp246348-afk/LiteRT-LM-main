# Redis Cache Layer

## 🌟 Overview

This project provides a robust and high-performance distributed caching layer using Redis. It's designed to dramatically reduce database load by serving frequently accessed data directly from memory. Built for scalability and speed, this layer ensures your application remains responsive even under heavy traffic.

## 🚀 Key Features

*   **High-Performance Caching:** Leverages Redis for lightning-fast data retrieval and storage.
*   **Reduced Database Load:** Offloads read operations from your primary database, improving overall application performance and reducing costs.
*   **Distributed Cache:** Enables seamless scaling across multiple application instances.
*   **Automatic Expiration:** Configurable Time-To-Live (TTL) for cache entries ensures data freshness.
*   **Environment Variable Configuration:** Flexible setup using `REDIS_CLUSTER_URL` for production environments, with a sensible default for local development.

## 🛠️ Installation & Setup

**Prerequisites:**

*   Python 3.6+
*   Redis server running locally or accessible via network.

**Installation:**

1.  **Install the Redis Python client:**
    ```bash
    pip install redis
    ```

**Configuration:**

*   **Development:** The cache will default to connecting to `redis://localhost:6379/0` if the `REDIS_CLUSTER_URL` environment variable is not set.
*   **Production:** It is **highly recommended** to set the `REDIS_CLUSTER_URL` environment variable to your Redis cluster's connection string.
    ```bash
    export REDIS_CLUSTER_URL="redis://your-redis-host:6379/0"
    ```

## 💻 Usage Instructions

To utilize the caching layer, instantiate the `MemoryLayer` class and then use its methods to interact with the cache.

1.  **Import the class:**
    ```python
    from redis_cache import MemoryLayer
    ```

2.  **Initialize the cache:**
    ```python
    cache = MemoryLayer()
    ```

3.  **Fetch data from the cache:**
    ```python
    cached_data = cache.fetch_fast("my_key")
    if cached_data:
        print(f"Data found in cache: {cached_data}")
    else:
        print("Data not in cache, fetching from source...")
        # Fetch data from your primary data source here
        # new_data = database.get("my_key")
        # if new_data:
        #     cache.write_fast("my_key", new_data)
    ```

4.  **Write data to the cache:**
    ```python
    cache.write_fast("my_key", "my_value")
    print("Data written to cache.")
    ```

## 🏗️ Architecture Design

The `redis_cache.py` module encapsulates the `MemoryLayer` class, which serves as the primary interface for interacting with the Redis caching system.

*   **`MemoryLayer` Class:**
    *   **`__init__(self)`:** The constructor initializes the connection to Redis. It attempts to read the `REDIS_CLUSTER_URL` environment variable for production configurations. If this variable is not set, it falls back to a default local Redis instance (`redis://localhost:6379/0`). Upon successful connection, a confirmation message is printed.
    *   **`fetch_fast(self, key)`:** This method retrieves data from Redis associated with the provided `key`. It returns the cached value directly if found, otherwise it returns `None`.
    *   **`write_fast(self, key, value)`:** This method stores the `value` in Redis under the specified `key`. The cache entry is configured to automatically expire after 3600 seconds (1 hour) to ensure data does not become stale.

This design promotes a clean separation of concerns, allowing developers to easily integrate caching logic into their applications without complex setup or deep knowledge of Redis internals.