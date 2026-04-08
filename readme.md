# Project Title: Temporary Data Store

## 🌟 Overview

This project provides a **Temporary Data Store** solution designed for managing short-lived data such as One-Time Passwords (OTPs) and authentication tokens. Leveraging the power and speed of Redis, this store ensures efficient storage and retrieval of ephemeral information, crucial for modern application security and user experience.

## 🚀 Key Features

*   **Short-Lived Data Management**: Optimized for storing data that has a limited validity period.
*   **Redis Integration**: Utilizes Redis as a high-performance backend for caching and temporary storage.
*   **Configurable Expiry**: Allows setting custom expiration times for stored data, defaulting to 120 seconds.
*   **Simple API**: Offers straightforward methods for saving, retrieving, and deleting temporary data.
*   **Environment Variable Configuration**: Supports setting the Redis connection URL via the `REDIS_CLUSTER_URL` environment variable for flexible deployment.

## 🛠️ Installation & Setup

To use the Temporary Data Store, you need to have Redis installed and accessible. 

### Prerequisites

*   Python 3.x
*   Redis server running

### Installation

1.  **Install Dependencies**: This project requires the `redis` Python package.
    ```bash
    pip install redis
    ```

2.  **Configure Redis Connection (Optional)**:
    By default, the store connects to `redis://localhost:6379/0`. If your Redis instance is located elsewhere, set the `REDIS_CLUSTER_URL` environment variable:
    ```bash
    export REDIS_CLUSTER_URL="redis://your-redis-host:6379/0"
    ```

## 💻 Usage Instructions

Instantiate the `TempStore` class and use its methods to manage your temporary data.

### Initializing the Store

```python
from temp_store import TempStore

store = TempStore()
```

### Saving Temporary Data

Use the `save_temp` method to store a key-value pair with an optional expiration time.

```python
# Save an OTP with a 60-second expiry
store.save_temp("user:123:otp", "123456", expiry=60)

# Save a session token with the default 120-second expiry
store.save_temp("user:123:token", "abcdef123456")
```

### Retrieving Temporary Data

Use the `get_temp` method to retrieve the value associated with a key.

```python

otp = store.get_temp("user:123:otp")
if otp:
    print(f"Retrieved OTP: {otp.decode('utf-8')}") # Note: Redis returns bytes
else:
    print("OTP not found or expired.")
```

### Deleting Temporary Data

Use the `delete_temp` method to remove a key-value pair from the store.

```python
store.delete_temp("user:123:token")
print("Session token deleted.")
```

## 🏗️ Architecture Design

The Temporary Data Store is built around a simple yet effective client-server architecture:

*   **Client**: The Python application utilizing the `TempStore` class.
*   **Data Store Backend**: A Redis instance serving as the primary storage mechanism.

**Data Flow**:

1.  **Initialization**: The `TempStore` class initializes by establishing a connection to the Redis server. The connection URL can be provided via an environment variable (`REDIS_CLUSTER_URL`) or defaults to a local Redis instance.
2.  **Operations**: When `save_temp`, `get_temp`, or `delete_temp` is called, the `TempStore` class acts as a thin client, translating these requests into commands executed against the Redis server via the `redis-py` library.
3.  **Persistence & Expiry**: Redis handles the actual storage, retrieval, and automatic expiration of keys based on the provided `ex` (expiration) parameter, ensuring that data is automatically removed after its intended lifespan.

This design prioritizes simplicity, performance, and scalability, making it ideal for use cases requiring fast access to time-sensitive data.