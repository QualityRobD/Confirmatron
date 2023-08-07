import unittest
from unittest.mock import MagicMock
from src.modules.constants import TestStatus
from src.modules.results import Results, TestResult


class TestResults(unittest.TestCase):

    def setUp(self):
        self.results = Results()
        self.redis_mock = MagicMock()
        self.results.redis_client = self.redis_mock

    def test_add_result(self):
        # Mocking Redis client methods
        self.redis_mock.store_result.return_value = None
        self.redis_mock.update_counters.return_value = None

        test_key = "test-api:32a4a415-5027-48e7-bec3-5a1c6b328b71"
        field = "test-31056241454"
        result = TestStatus.PASS
        payload_sent = {"data": "sent"}
        payload_received = {"data": "received"}
        context = "Some context"

        # Perform the add_result method call
        self.results.add_result(test_key, field, result, payload_sent, payload_received, context)

        # Assert that Redis client methods were called with correct arguments
        self.redis_mock.store_result.assert_called_once_with(test_key, field, result, payload_sent, payload_received,
                                                             context)
        self.redis_mock.update_counters.assert_called_once_with(result)

    def test_get_total_tests(self):
        # Mocking Redis client method
        self.redis_mock.get_total.return_value = 100

        # Perform the get_total_tests method call
        total_tests = self.results.get_total_tests()

        # Assert the returned value is correct
        self.assertEqual(total_tests, 100)
        # Assert that Redis client method was called with correct argument
        self.redis_mock.get_total.assert_called_once_with("total_tests")

    def test_get_total_pass(self):
        # Mocking Redis client method
        self.redis_mock.get_total.return_value = 50

        # Perform the get_total_pass method call
        total_pass = self.results.get_total_pass()

        # Assert the returned value is correct
        self.assertEqual(total_pass, 50)
        # Assert that Redis client method was called with correct argument
        self.redis_mock.get_total.assert_called_once_with("total_pass")

    def test_get_total_fail(self):
        # Mocking Redis client method
        self.redis_mock.get_total.return_value = 25

        # Perform the get_total_fail method call
        total_fail = self.results.get_total_fail()

        # Assert the returned value is correct
        self.assertEqual(total_fail, 25)
        # Assert that Redis client method was called with correct argument
        self.redis_mock.get_total.assert_called_once_with("total_fail")

    def test_get_result(self):
        # Mocking Redis client method
        test_key = "test-api:32a4a415-5027-48e7-bec3-5a1c6b328b71"
        field = "test-31056241454"
        result_value = TestStatus.PASS.value
        self.redis_mock.retrieve_results.return_value = {field: result_value}

        # Perform the get_result method call
        result = self.results.get_result(test_key, field)

        # Assert the returned value is correct
        self.assertEqual(result, TestStatus.PASS)
        # Assert that Redis client method was called with correct argument
        self.redis_mock.retrieve_results.assert_called_once_with(test_key)

    # Add more test cases for other methods, if needed.


class TestTestResult(unittest.TestCase):

    def setUp(self):
        self.test_key = "test-api:32a4a415-5027-48e7-bec3-5a1c6b328b71"
        self.test_result = TestResult(self.test_key)
        self.redis_mock = MagicMock()
        self.test_result.redis_client = self.redis_mock

    def test_status(self):
        # Mocking Redis client method
        self.redis_mock.store_result.return_value = None
        self.redis_mock.incr.return_value = None

        # Set the status of the test
        self.test_result.status = TestStatus.PASS

        # Assert that Redis client method was called with correct arguments
        self.redis_mock.store_result.assert_called_once_with(
            self.test_key,
            "status",
            TestStatus.PASS,
            self.test_result._payload_sent,
            self.test_result._payload_received,
            self.test_result._context
        )
        self.redis_mock.incr.assert_called_once_with("total_tests")
        self.redis_mock.incr.assert_called_once_with("total_pass")

    # Add more test cases for other methods and properties, if needed.


if __name__ == '__main__':
    unittest.main()
