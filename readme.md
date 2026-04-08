# Temporary Data Store

## 🌟 Overview

This project provides a simple yet powerful **Temporary Data Store** solution, designed for managing short-lived data such as One-Time Passwords (OTPs), session tokens, or any other ephemeral information that needs to be stored and retrieved quickly with a defined expiration.

Leveraging the speed and efficiency of Redis, this data store is ideal for applications requiring robust caching and temporary data management without the overhead of persistent database solutions for transient data.

## 🚀 Key Features

*   **Ephemeral Data Storage**: Optimized for data that has a limited lifespan.
*   **Redis Integration**: Built on top of Redis for high performance and scalability.
*   **Simple API**: Easy-to-use methods for saving, retrieving, and deleting temporary data.
*   **Configurable Expiry**: Set custom expiration times for each piece of data.
*   **Environment Variable Configuration**: Flexible connection to Redis instances via `REDIS_CLUSTER_URL` environment variable.

## 🛠️ Installation & Setup

**Prerequisites**:

*   Python 3.7+
*   Redis server instance running

**Installation**:

1.  **Clone the repository**:
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Ensure `redis` is listed in your `requirements.txt` or install it directly: `pip install redis`)*

3.  **Configure Redis Connection**:
    By default, the `TempStore` will attempt to connect to `redis://localhost:6379/0`. To use a different Redis instance (e.g., a Redis Cluster), set the `REDIS_CLUSTER_URL` environment variable before running your application:

    ```bash
    export REDIS_CLUSTER_URL="redis://your-redis-host:6379/0"
    ```

## 💻 Usage Instructions

### Initializing the Data Store

Instantiate the `TempStore` class to connect to your Redis instance.

```python
from temp_store import TempStore

temp_store = TempStore()
print("TempStore initialized and connected to Redis.")
```

### Saving Temporary Data

Use the `save_temp` method to store a key-value pair with an optional expiration time (in seconds).

```python
# Save with default expiry (120 seconds)
temp_store.save_temp("user:123:otp", "123456")

# Save with a custom expiry (e.g., 300 seconds / 5 minutes)
temp_store.save_temp("session:abc", "user_session_token", expiry=300)
```

### Retrieving Temporary Data

Use the `get_temp` method to retrieve the value associated with a key.

```python
otp = temp_store.get_temp("user:123:otp")
if otp:
    print(f"Retrieved OTP: {otp.decode('utf-8')}") # Redis returns bytes
else:
    print("OTP not found or expired.")
```

### Deleting Temporary Data

Use the `delete_temp` method to explicitly remove a key-value pair from the store.

```python
if temp_store.delete_temp("user:123:otp"):
    print("OTP deleted successfully.")
```

## 🏗️ Architecture Design

The `TempStore` class acts as a client interface to a Redis backend. The design prioritizes simplicity and direct interaction with Redis commands for temporary data operations.

*   **`__init__`**: Initializes the connection to Redis. It attempts to read the Redis connection URL from the `REDIS_CLUSTER_URL` environment variable, falling back to a default local Redis instance (`redis://localhost:6379/0`). This provides flexibility in deployment scenarios.
*   **`save_temp(key, value, expiry)`**: Utilizes Redis's `SET` command with the `EX` option. This atomically sets a key-value pair and assigns it a Time To Live (TTL) in seconds, ensuring the data is automatically removed after the specified duration.
*   **`get_temp(key)`**: Uses Redis's `GET` command to retrieve the value associated with a given key. If the key does not exist or has expired, Redis returns `None`.
*   **`delete_temp(key)`**: Employs Redis's `DEL` command to remove a key from the store. This is useful for explicitly invalidating temporary data before its natural expiration.

This architecture ensures that all temporary data operations are handled efficiently by Redis, providing low latency and reliable ephemeral storage.
