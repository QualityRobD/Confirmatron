import os
import redis
import uuid
from typing import Dict, List
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

    def retrieve_results(self, key: str) -> Dict[str, str]:
        """
        Retrieve all fields and their values associated with the provided key from Redis.

        Args:
            key (str): The key in Redis from which to retrieve the results.

        Returns:
            Dict[str, str]: A dictionary of field-value pairs from the Redis hash.
        """
        return {field.decode('utf-8'): value.decode('utf-8') for field, value in self.redis_client.hgetall(key).items()}

    def store_result(self, key: str, field: str, result: TestStatus):
        """
        Store a test result in Redis.

        Args:
            key (str): The key in Redis where the test result will be stored.
            field (str): The field name under which the result will be stored within the hash.
            result (TestStatus): The test result status (PASS or FAIL).

        Raises:
            redis.exceptions.RedisError: If there is an issue with the Redis connection or storage.

        Returns:
            None
        """
        data_to_store = JsonUtility.to_string(result.value)
        self.redis_client.hset(key, field, data_to_store)
        self.redis_client.expire(key, self.expire_seconds)

    def update_counters(self, result: TestStatus) -> None:
        """
        Update the counters in Redis that keep track of the total number of passed and failed tests.

        Args:
            result (TestStatus): The test result based on which to increment the counter.
        """
        if result == TestStatus.PASS:
            self.redis_client.incr('total_pass')
        else:
            self.redis_client.incr('total_fail')

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
