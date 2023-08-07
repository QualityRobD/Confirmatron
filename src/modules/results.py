from typing import Dict, Any
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

    def add_result(self, key: str, field: str, result: TestStatus,
                   payload_sent: Dict[str, Any], payload_received: Dict[str, Any], context: str):
        """
        Add a test result to the Redis database and update the counters.

        Args:
            key (str): The key identifying the test.
            field (str): The field where the result should be stored.
            result (TestStatus): The test result to store.
            payload_sent (dict): The payload sent during the test.
            payload_received (dict): The payload received during the test.
            context (str): Additional context or reason for the test result.
        """
        self.redis_client.store_result(key, field, result, payload_sent, payload_received, context)

    def get_total_tests(self) -> int:
        """
        Get the total number of tests performed.

        Returns:
            int: The total number of tests.
        """
        return self.redis_client.get_total("total_tests")

    def get_total_pass(self) -> int:
        """
        Get the total number of passed tests.

        Returns:
            int: The total number of passed tests.
        """
        return self.redis_client.get_total("total_pass")

    def get_total_fail(self) -> int:
        """
        Get the total number of failed tests.

        Returns:
            int: The total number of failed tests.
        """
        return self.redis_client.get_total("total_fail")

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


class TestResult:
    """
    A class representing the result of a test.

    Attributes:
        redis_client (RedisClient): The RedisClient instance to interact with Redis.
        test_key (str): The unique key associated with the test result in Redis.
        _status (TestStatus): The status of the test (PASS or FAIL).
        _payload_sent (Dict[str, Any]): The payload sent during the test, if applicable.
        _payload_received (Dict[str, Any]): The payload received during the test, if applicable.
        _context (str): Additional context or information about the test result.

    Methods:
        _update_counters(): Update the counters for total_tests, total_pass, and total_fail in Redis.
    """

    def __init__(self, test_key: str):
        """
        Initialize a TestResult object.

        Args:
            test_key (str): The unique key associated with the test result in Redis.
        """
        self.redis_client = RedisClient()
        self.test_key = test_key
        self._status = None
        self._payload_sent = {}
        self._payload_received = {}
        self._context = ""

    @property
    def status(self) -> TestStatus:
        """
        Get the status of the test.

        Returns:
            TestStatus: The status of the test (PASS or FAIL).
        """
        return self._status

    @status.setter
    def status(self, value: TestStatus):
        """
        Set the status of the test and update it in Redis.

        Args:
            value (TestStatus): The status of the test (PASS or FAIL).
        """
        self._status = value
        self.redis_client.store_result(
            self.test_key,
            "status",
            value,
            self._payload_sent,
            self._payload_received,
            self._context,
        )

        # Update the counters for total_tests, total_pass, and total_fail
        self._update_counters()

    @property
    def payload_sent(self) -> Dict[str, Any]:
        """
        Get the payload sent during the test.

        Returns:
            dict: The payload sent during the test.
        """
        return self._payload_sent

    @payload_sent.setter
    def payload_sent(self, value: Dict[str, Any]):
        """
        Set the payload sent during the test and update it in Redis.

        Args:
            value (dict): The payload sent during the test.
        """
        self._payload_sent = value
        self.redis_client.store_result(
            self.test_key,
            "payload_sent",
            self._status,
            value,
            self._payload_received,
            self._context,
        )

    @property
    def payload_received(self) -> Dict[str, Any]:
        """
        Get the payload received during the test.

        Returns:
            dict: The payload received during the test.
        """
        return self._payload_received

    @payload_received.setter
    def payload_received(self, value: Dict[str, Any]):
        """
        Set the payload received during the test and update it in Redis.

        Args:
            value (dict): The payload received during the test.
        """
        self._payload_received = value
        self.redis_client.store_result(
            self.test_key,
            "payload_received",
            self._status,
            self._payload_sent,
            value,
            self._context,
        )

    @property
    def context(self) -> str:
        """
        Get the additional context or reason for the test result.

        Returns:
            str: The additional context or reason for the test result.
        """
        return self._context

    @context.setter
    def context(self, value: str):
        """
        Set the additional context or reason for the test result and update it in Redis.

        Args:
            value (str): The additional context or reason for the test result.
        """
        self._context = value
        self.redis_client.store_result(
            self.test_key,
            "context",
            self._status,
            self._payload_sent,
            self._payload_received,
            value,
        )

    def _update_counters(self):
        """
        Update the counters for total_tests, total_pass, and total_fail in Redis based on the test status.
        """
        total_tests_key = "total_tests"
        total_pass_key = "total_pass"
        total_fail_key = "total_fail"

        self.redis_client.incr(total_tests_key)
        if self._status == TestStatus.PASS:
            self.redis_client.incr(total_pass_key)
        elif self._status == TestStatus.FAIL:
            self.redis_client.incr(total_fail_key)
