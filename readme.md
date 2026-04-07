# Redis Data Caching Layer

## 🌟 Overview

This project provides a high-performance distributed caching layer using Redis. It's designed to dramatically reduce database load by serving frequently accessed data from a fast, in-memory cache. This layer is essential for applications demanding low latency and high throughput, ensuring a seamless user experience.

## 🚀 Key Features

*   **High-Performance Caching:** Leverages Redis for lightning-fast data retrieval and storage.
*   **Distributed Architecture:** Seamlessly scales with your application by utilizing Redis's distributed nature.
*   **Reduced Database Load:** Offloads read operations from your primary database, improving overall system performance and stability.
*   **Configurable Expiration:** Data can be set with Time-To-Live (TTL) to ensure freshness and prevent stale data.
*   **Environment Variable Configuration:** Easily configure Redis connection details using environment variables for flexible deployment.

## 🛠️ Installation & Setup

This caching layer requires the `redis` Python package. Install it using pip:

```bash
pip install redis
```

### Environment Configuration

For production environments, it is **critical** to set the `REDIS_CLUSTER_URL` environment variable to point to your Redis cluster. For local development, the system will default to `redis://localhost:6379/0`.

**Example (Linux/macOS):**

```bash
export REDIS_CLUSTER_URL="redis://your-redis-host:6379/0"
```

**Example (Windows):**

```bash
set REDIS_CLUSTER_URL="redis://your-redis-host:6379/0"
```

## 💻 Usage Instructions

To integrate the caching layer into your application, instantiate the `MemoryLayer` class and use its methods to interact with the cache.

### Initialization

```python
from redis_cache import MemoryLayer

# Initialize the cache layer
cache = MemoryLayer()
```

### Fetching Data

Use the `fetch_fast` method to retrieve data from the cache using a unique key.

```python
user_data = cache.fetch_fast("user:123")
if user_data:
    print("Data found in cache!")
    # Process user_data
else:
    print("Data not found in cache. Fetching from DB...")
    # Fetch data from the database and then write it to the cache
```

### Writing Data

Use the `write_fast` method to store data in the cache. Data will automatically expire after 1 hour (3600 seconds).

```python
new_user_profile = {"name": "Alice", "email": "alice@example.com"}
cache.write_fast("user:456", str(new_user_profile)) # Values are typically stored as strings or bytes
print("User profile cached!")
```

## 🏗️ Architecture Design

The caching layer is implemented as a simple `MemoryLayer` class. This class abstracts the complexities of interacting with Redis, providing a clean interface for common caching operations.

*   **`__init__(self)`:** Initializes the connection to the Redis cache. It attempts to use the `REDIS_CLUSTER_URL` environment variable for configuration, falling back to a local Redis instance if the variable is not set.
*   **`fetch_fast(self, key)`:** Retrieves a value from Redis associated with the provided `key`. Returns the value if found, otherwise `None`.
*   **`write_fast(self, key, value)`:** Stores a `value` in Redis under the given `key`. The entry is automatically configured to expire after 1 hour (`ex=3600`).

This design promotes separation of concerns, allowing the core application logic to remain independent of the caching mechanism. The use of a dedicated class makes it easy to swap out or enhance the caching strategy in the future without significant changes to the rest of the codebase.