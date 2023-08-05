import os
import redis
import uuid
from typing import Dict, List, Any, Optional
from modules.constants import TestStatus
from modules.json_utility import JsonUtility


class RedisClient:
    """
    RedisClient is a wrapper around the redis-py StrictRedis client,
    providing some additional methods for managing test results in a Redis database.
    """

    def __init__(self):
        """
        Initialize RedisClient with a connection to the Redis server.
        Connection details are pulled from environment variables.
        """
        self.expire_seconds = 7200

        # Get Redis host and port from environment variables or Kubernetes secrets
        _redis_host = os.environ.get("REDIS_HOST", "localhost")  # Replace "localhost" with the default Redis host if needed
        _redis_port = int(os.environ.get("REDIS_PORT", 6379))  # Replace 6379 with the default Redis port if needed

        # Create the Redis client with the obtained host and port
        self.redis_client = redis.StrictRedis(host=_redis_host, port=_redis_port, db=0)

    def create_key(self, api_name: str) -> str:
        """
        Create a unique key for each test in Redis hash.

        Args:
            api_name (str): The name of the API for which the key is being created.

        Returns:
            str: The unique key created for the test.
        """
        unique_id = str(uuid.uuid4())
        key = f"{api_name}:{unique_id}"
        self.redis_client.hset(key, "Tests Initialized", "")
        self.redis_client.expire(key, self.expire_seconds)
        return key

    def initialize_test_suite(self, key: str):
        """
        Initialize the test suite by setting initial values for total_tests, total_pass, and total_fail.

        Args:
            key (str): The key of the test suite in Redis.
        """

        self.redis_client.hset(key, "total_tests", 0)
        self.redis_client.hset(key, "total_pass", 0)
        self.redis_client.hset(key, "total_fail", 0)

    def retrieve_results(self, key: str) -> Dict[str, str]:
        """
        Retrieve all fields and their values associated with the provided key from Redis.

        Args:
            key (str): The key in Redis from which to retrieve the results.

        Returns:
            Dict[str, str]: A dictionary of field-value pairs from the Redis hash.
        """
        return {field.decode('utf-8'): value.decode('utf-8') for field, value in self.redis_client.hgetall(key).items()}

    def get_total(self, key: str) -> Optional[int]:
        """
        Get the total count from Redis.

        Args:
            key (str): The key to fetch the total count for.

        Returns:
            int or None: The total count value, or None if the key does not exist.
        """
        return self.redis_client.get(key)

    def store_result(self, key: str, field: str, result: TestStatus, payload_sent: Dict[str, Any],
                     payload_received: Dict[str, Any], context: str):
        """
        Store a test result in Redis.

        Args:
            key (str): The key in Redis where the test result will be stored.
            field (str): The field name under which the result will be stored within the hash.
            result (TestStatus): The test result status (PASS or FAIL).
            payload_sent (dict): The payload sent during the test.
            payload_received (dict): The payload received during the test.
            context (str): Additional context or reason for the test result.

        Raises:
            redis.exceptions.RedisError: If there is an issue with the Redis connection or storage.

        Returns:
            None
        """
        data_to_store = {
            "status": result.value,
            "payload_sent": payload_sent,
            "payload_received": payload_received,
            "context": context,
        }
        data_to_store_str = JsonUtility.serialize(data_to_store)
        self.redis_client.hset(key, field, data_to_store_str)
        self.redis_client.expire(key, self.expire_seconds)

        # Update the total counters based on the test result
        self.update_counters(result, key)

    def update_counters(self, result: TestStatus, key: str):
        """
        Update the total counters based on the test result.

        Args:
            result (TestStatus): The test result status (PASS or FAIL).
            key (str): The key identifying the test.

        Raises:
            redis.exceptions.RedisError: If there is an issue with the Redis connection or storage.
        """

        self.redis_client.hincrby(key, "total_tests", 1)
        if result == TestStatus.PASS:
            self.redis_client.hincrby(key, "total_pass", 1)
        elif result == TestStatus.FAIL:
            self.redis_client.hincrby(key, "total_fail", 1)

    def get_redis_keys(self, api_name: str) -> List[str]:
        """
        Retrieve all keys in Redis that match the provided API name.

        Args:
            api_name (str): The name of the API for which to retrieve the keys.

        Returns:
            List[str]: A list of keys from Redis that match the provided API name.
        """
        all_keys = self.redis_client.keys(f"{api_name}:*")
        return [key.decode("utf-8") for key in all_keys]

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in Redis.

        Args:
            key (str): The key to check in Redis.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return bool(self.redis_client.exists(key))

    def incr(self, key):
        """
        Increment the value stored in the Redis key by 1.

        Args:
            key (str): The Redis key to increment.

        Returns:
            int: The new value after the increment.
        """
        return self.redis_client.incr(key)
