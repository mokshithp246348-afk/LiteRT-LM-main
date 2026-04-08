# Temp Data Store

## 🌟 Overview

Welcome to the Temp Data Store project! This repository provides a robust and efficient solution for managing short-lived data, such as One-Time Passwords (OTPs) or authentication tokens. Built with reliability and performance in mind, it leverages Redis to ensure fast access and automatic expiration of your temporary data.

## 🚀 Key Features

*   **Ephemeral Data Management:** Ideal for storing sensitive, time-bound information that should not persist indefinitely.
*   **Redis Integration:** Utilizes Redis for high-speed data retrieval and storage, ensuring minimal latency.
*   **Configurable Expiry:** Easily set expiration times for your temporary data, ensuring automatic cleanup.
*   **Simple API:** A clean and intuitive interface for saving, retrieving, and deleting temporary data.

## 🛠️ Installation & Setup

This project requires Python and Redis to be installed.

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install Dependencies:**
    ```bash
    pip install redis
    ```

3.  **Configure Redis:**
    Ensure a Redis instance is running and accessible. By default, the application attempts to connect to `redis://localhost:6379/0`. You can configure the Redis connection URL by setting the `REDIS_CLUSTER_URL` environment variable.
    ```bash
    export REDIS_CLUSTER_URL="redis://your_redis_host:port/db_number"
    ```

## 💻 Usage Instructions

To use the `TempStore` class, follow these steps:

1.  **Instantiate the Store:**
    ```python
    from temp_store import TempStore

    store = TempStore()
    ```

2.  **Save Temporary Data:**
    Use the `save_temp` method to store a key-value pair with an optional expiry time (in seconds).
    ```python
    store.save_temp("user:123:otp", "123456", expiry=120) # Expires in 120 seconds
    ```

3.  **Retrieve Temporary Data:**
    Use the `get_temp` method to retrieve the value associated with a key.
    ```python
    otp_code = store.get_temp("user:123:otp")
    if otp_code:
        print(f"Retrieved OTP: {otp_code.decode('utf-8')}") # Redis stores bytes, decode to string
    else:
        print("OTP not found or expired.")
    ```

4.  **Delete Temporary Data:**
    Use the `delete_temp` method to manually remove a key-value pair.
    ```python
    store.delete_temp("user:123:otp")
    ```

## 🏗️ Architecture Design

The `TempStore` class is designed for simplicity and efficiency. It acts as a thin client wrapper around the Redis client library.

*   **`__init__(self)`:** Initializes the connection to Redis. It reads the Redis connection URL from the `REDIS_CLUSTER_URL` environment variable, defaulting to `redis://localhost:6379/0` if the variable is not set. A confirmation message is printed upon successful connection.
*   **`save_temp(self, key, value, expiry=120)`:** This method utilizes Redis's `SET` command with the `EX` option to store the `key`-`value` pair. The `expiry` parameter, defaulting to 120 seconds, defines the Time To Live (TTL) for the stored item. It returns `True` upon successful storage.
*   **`get_temp(self, key)`:** This method uses Redis's `GET` command to retrieve the value associated with the given `key`. It returns the value as bytes, or `None` if the key does not exist or has expired.
*   **`delete_temp(self, key)`:** This method employs Redis's `DELETE` command to remove the specified `key` and its associated value from the store. It returns `True` upon successful deletion.