# TempDataStore

## 🌟 Overview

Welcome to TempDataStore, a robust and efficient temporary data storage solution designed for short-lived data such as One-Time Passwords (OTPs) and authentication tokens. Leveraging the speed and reliability of Redis, TempDataStore provides a seamless way to manage ephemeral data crucial for modern application security and user flows.

## 🚀 Key Features

*   **Ephemeral Data Management**: Specifically designed for data with a limited lifespan.
*   **Redis Integration**: Utilizes Redis for high-performance, in-memory data storage.
*   **Configurable Expiry**: Easily set expiration times for stored data to ensure automatic cleanup.
*   **Simple API**: Intuitive methods for saving, retrieving, and deleting temporary data.
*   **Environment Variable Configuration**: Flexible setup via `REDIS_CLUSTER_URL` environment variable.

## 🛠️ Installation & Setup

### Prerequisites

*   **Python 3.6+**
*   **Redis Server**: Ensure a Redis server is running and accessible.

### Installation

1.  **Install Redis Python Client**: 
    ```bash
    pip install redis
    ```

### Configuration

By default, TempDataStore attempts to connect to `redis://localhost:6379/0`. You can customize the Redis connection URL by setting the `REDIS_CLUSTER_URL` environment variable:

```bash
export REDIS_CLUSTER_URL="redis://your_redis_host:your_redis_port/db_number"
```

## 💻 Usage Instructions

### Initialization

Create an instance of the `TempStore` class. The constructor will attempt to connect to Redis based on the configuration.

```python
from temp_store import TempStore

temp_store = TempStore()
```

### Saving Temporary Data

Use the `save_temp` method to store a key-value pair with an optional expiration time (in seconds). The default expiry is 120 seconds.

```python
# Save a token with default expiry (120 seconds)
temp_store.save_temp("user_session_123", "auth_token_abc")

# Save an OTP with a custom expiry of 30 seconds
temp_store.save_temp("user_otp_456", "123456", expiry=30)
```

### Retrieving Temporary Data

Use the `get_temp` method to retrieve the value associated with a given key.

```python
token = temp_store.get_temp("user_session_123")
if token:
    print(f"Retrieved token: {token.decode('utf-8')}") # Redis returns bytes


otp = temp_store.get_temp("user_otp_456")
if otp:
    print(f"Retrieved OTP: {otp.decode('utf-8')}")
```

### Deleting Temporary Data

Use the `delete_temp` method to manually remove a key-value pair from the store before its expiration.

```python
temp_store.delete_temp("user_session_123")
print("Deleted user session.")
```

## 🏗️ Architecture Design

The TempDataStore is built around a simple, yet effective, architecture centered on the `TempStore` class. This class acts as the primary interface for interacting with the temporary data backend.

*   **Core Component**: The `TempStore` class encapsulates all logic for data persistence and retrieval.
*   **Backend Integration**: It directly integrates with the `redis-py` library to communicate with a Redis server.
*   **Configuration**: Connection details for Redis are managed through the `REDIS_CLUSTER_URL` environment variable, allowing for flexible deployment scenarios. If not specified, it defaults to a local Redis instance.
*   **Data Lifecycle**: Data is stored with a Time-To-Live (TTL) mechanism provided by Redis, ensuring that entries are automatically removed after their specified `expiry` period. Manual deletion is also supported.

This design prioritizes simplicity, performance, and ease of integration, making it suitable for applications requiring fast access to short-lived data.
