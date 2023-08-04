from modules.constants import TestStatus
from modules.redis_client import RedisClient

class Results:
    """
    The TestResult class provides methods for storing and managing test results in a Redis database.
    """
    def __init__(self):
        """
        Initialize a new instance of the TestResult class.
        """
        self.redis_client = RedisClient()

    def add_result(self, test_key: str, field: str, result: TestStatus):
        """
        Add a test result to the Redis database and update the counters.

        Args:
            test_key (str): The key identifying the test.
            field (str): The field where the result should be stored.
            result (TestStatus): The test result to store.
        """
        self.redis_client.store_result(test_key, field, result)
        self.redis_client.update_counters(result)

    def get_result(self, test_key: str, field: str) -> TestStatus:
        """
        Get a specific test result by its key and field.

        Args:
            test_key (str): The key identifying the test.
            field (str): The field where the result is stored.

        Returns:
            TestStatus: The requested test result.
        """
        result = self.redis_client.retrieve_results(test_key).get(field, None)
        return TestStatus(result) if result else None

    def update_result(self, test_key: str, field: str, new_result: TestStatus):
        """
        Update a specific test result and update the counters.

        Args:
            test_key (str): The key identifying the test.
            field (str): The field where the result is stored.
            new_result (TestStatus): The new test result to store.
        """
        if self.redis_client.exists(test_key):
            self.redis_client.store_result(test_key, field, new_result)
            self.redis_client.update_counters(new_result)

    def get_results_by_key(self, test_key: str):
        """
        Get all the results of a specific test by its key.

        Args:
            test_key (str): The key identifying the test.

        Returns:
            dict: The test results, where each key is a field name and each value is a result.
        """
        return self.redis_client.retrieve_results(test_key)

    def get_all_keys(self, api_name: str):
        """
        Get all the keys related to a specific api.

        Args:
            api_name (str): The name of the API.

        Returns:
            list: A list of keys related to the API.
        """
        return self.redis_client.get_redis_keys(api_name)
