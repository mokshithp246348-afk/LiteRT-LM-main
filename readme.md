# Temp Data Store

## 🌟 Overview

Welcome to the **Temp Data Store** project! This repository provides a robust and efficient solution for managing short-lived data such as One-Time Passwords (OTPs), session tokens, and other temporary information. Built with a focus on performance and reliability, it leverages Redis to ensure fast access and automatic expiration of your transient data.

This project is designed to be a core component in applications requiring secure and time-sensitive data handling, ensuring that sensitive information is only available for the necessary duration.

## 🚀 Key Features

*   **Ephemeral Data Storage**: Securely store data that needs to expire after a set period.
*   **Redis Integration**: Utilizes Redis for high-speed, in-memory data persistence and retrieval.
*   **Configurable Expiry**: Easily set custom expiration times for each stored item.
*   **Simple API**: Intuitive methods for saving, retrieving, and deleting temporary data.
*   **Environment Variable Configuration**: Supports dynamic Redis connection string configuration via `REDIS_CLUSTER_URL` environment variable.

## 🛠️ Installation & Setup

### Prerequisites

*   **Python**: Ensure you have Python 3.6+ installed.
*   **Redis**: A Redis instance must be running and accessible. You can run it locally or use a managed Redis service.

### Installation Steps

1.  **Clone the Repository**: 
    ```bash
    git clone <your-repository-url>
    cd temp-data-store
    ```

2.  **Install Dependencies**: 
    This project relies on the `redis` Python library.
    ```bash
    pip install redis
    ```

3.  **Configure Redis Connection (Optional)**:
    By default, the store connects to `redis://localhost:6379/0`. If your Redis instance is located elsewhere or requires different credentials, set the `REDIS_CLUSTER_URL` environment variable:
    ```bash
    export REDIS_CLUSTER_URL="redis://<your-redis-host>:<your-redis-port>/<db-number>"
    ```

## 💻 Usage Instructions

To use the `TempStore` class, instantiate it and then utilize its methods:

```python
from temp_store import TempStore

# Initialize the temporary data store
temp_store = TempStore()

# Save a value with a default expiry of 120 seconds
temp_store.save_temp("user:123:otp", "123456")

# Save a value with a custom expiry of 300 seconds
temp_store.save_temp("session:abc", "session_token_data", expiry=300)

# Retrieve a value
retrieved_otp = temp_store.get_temp("user:123:otp")
if retrieved_otp:
    print(f"Retrieved OTP: {retrieved_otp.decode('utf-8')}") # Note: Redis returns bytes
else:
    print("OTP not found or expired.")

# Delete a value
temp_store.delete_temp("user:123:otp")

# Attempt to retrieve after deletion
retrieved_otp_after_delete = temp_store.get_temp("user:123:otp")
if not retrieved_otp_after_delete:
    print("OTP successfully deleted.")
```

## 🏗️ Architecture Design

The `TempDataStore` is designed around a simple, yet effective, client-server architecture leveraging Redis as the backend.

*   **`TempStore` Class**: This is the primary interface for interacting with the data store. It encapsulates all logic related to connecting to Redis and performing data operations.
    *   **`__init__(self)`**: Initializes the connection to Redis. It attempts to read the Redis connection URL from the `REDIS_CLUSTER_URL` environment variable, falling back to a default local Redis instance if the variable is not set. It establishes a connection using the `redis-py` library.
    *   **`save_temp(self, key, value, expiry=120)`**: This method takes a `key`, a `value`, and an optional `expiry` time (in seconds). It uses the Redis `SET` command with the `EX` option to store the key-value pair and set its Time To Live (TTL). This ensures the data is automatically removed after the specified duration.
    *   **`get_temp(self, key)`**: Retrieves the value associated with a given `key` from Redis. If the key exists and has not expired, its value is returned. Otherwise, it returns `None` (or rather, Redis's representation of a non-existent key, which `redis-py` typically maps to `None`).
    *   **`delete_temp(self, key)`**: Removes a key-value pair from Redis using the `DEL` command. This is useful for manually invalidating temporary data before its natural expiration.
*   **Redis**: Acts as the high-performance, in-memory data store. It handles the actual storage, retrieval, and expiration of data, providing the speed and reliability necessary for temporary data management.

This architecture is lightweight, scalable, and easy to integrate into existing applications, providing a dedicated service for managing time-sensitive information.
