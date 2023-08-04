import unittest
import os
import redis
from unittest.mock import MagicMock, patch
from my_module import RedisClient, TestStatus


class TestRedisClient(unittest.TestCase):

    def setUp(self):
        self.redis_client = RedisClient()

    @patch('redis.StrictRedis')
    def test_create_key(self, mock_strict_redis):
        api_name = "test-api"
        unique_id = "32a4a415-5027-48e7-bec3-5a1c6b328b71"
        mock_uuid4 = MagicMock(return_value=unique_id)
        with patch('uuid.uuid4', mock_uuid4):
            key = self.redis_client.create_key(api_name)
            expected_key = f"{api_name}:{unique_id}"
            self.assertEqual(key, expected_key)
            mock_strict_redis.return_value.hset.assert_called_once_with(expected_key, "Tests Initialized", "")
            mock_strict_redis.return_value.expire.assert_called_once_with(expected_key, self.redis_client.expire_seconds)

    @patch('redis.StrictRedis')
    def test_initialize_test_suite(self, mock_strict_redis):
        key = "test-api:32a4a415-5027-48e7-bec3-5a1c6b328b71"
        self.redis_client.initialize_test_suite(key)
        mock_strict_redis.return_value.hset.assert_any_call(key, "total_tests", 0)
        mock_strict_redis.return_value.hset.assert_any_call(key, "total_pass", 0)
        mock_strict_redis.return_value.hset.assert_any_call(key, "total_fail", 0)

    @patch('redis.StrictRedis')
    def test_retrieve_results(self, mock_strict_redis):
        key = "test-api:32a4a415-5027-48e7-bec3-5a1c6b328b71"
        data_to_return = {
            b"status": b"pass",
            b"payload_sent": b'{"data": "sent"}',
            b"payload_received": b'{"data": "received"}',
            b"context": b"Some context"
        }
        expected_results = {
            "status": "pass",
            "payload_sent": {"data": "sent"},
            "payload_received": {"data": "received"},
            "context": "Some context"
        }
        mock_strict_redis.return_value.hgetall.return_value = data_to_return
        results = self.redis_client.retrieve_results(key)
        self.assertEqual(results, expected_results)

    @patch('redis.StrictRedis')
    def test_get_total(self, mock_strict_redis):
        key = "test-api:32a4a415-5027-48e7-bec3-5a1c6b328b71"
        mock_strict_redis.return_value.get.return_value = b"10"
        total_tests = self.redis_client.get_total(key)
        self.assertEqual(total_tests, 10)

    @patch('redis.StrictRedis')
    def test_store_result(self, mock_strict_redis):
        key = "test-api:32a4a415-5027-48e7-bec3-5a1c6b328b71"
        field = "test-31056241454"
        result = TestStatus.PASS
        payload_sent = {"data": "sent"}
        payload_received = {"data": "received"}
        context = "Some context"
        expected_data_to_store = {
            "status": "pass",
            "payload_sent": {"data": "sent"},
            "payload_received": {"data": "received"},
            "context": "Some context"
        }
        expected_data_to_store_str = '{"status": "pass", "payload_sent": {"data": "sent"}, "payload_received": {"data": "received"}, "context": "Some context"}'
        mock_strict_redis.return_value.hset.return_value = None
        self.redis_client.store_result(key, field, result, payload_sent, payload_received, context)
        mock_strict_redis.return_value.hset.assert_called_once_with(key, field, expected_data_to_store_str)
        mock_strict_redis.return_value.expire.assert_called_once_with(key, self.redis_client.expire_seconds)
        mock_strict_redis.return_value.hincrby.assert_called_once_with(key, "total_tests", 1)

    @patch('redis.StrictRedis')
    def test_update_counters(self, mock_strict_redis):
        key = "test-api:32a4a415-5027-48e7-bec3-5a1c6b328b71"
        result = TestStatus.PASS
        self.redis_client.update_counters(result, key)
        mock_strict_redis.return_value.hincrby.assert_called_once_with(key, "total_tests", 1)
        mock_strict_redis.return_value.hincrby.assert_called_with(key, "total_pass", 1)

    @patch('redis.StrictRedis')
    def test_get_redis_keys(self, mock_strict_redis):
        api_name = "test-api"
        mock_strict_redis.return_value.keys.return_value = [b"test-api:32a4a415-5027-48e7-bec3-5a1c6b328b71"]
        keys = self.redis_client.get_redis_keys(api_name)
        self.assertEqual(keys, ["test-api:32a4a415-5027-48e7-bec3-5a1c6b328b71"])

    @patch('redis.StrictRedis')
    def test_exists(self, mock_strict_redis):
        key = "test-api:32a4a415-5027-48e7-bec3-5a1c6b328b71"
        mock_strict_redis.return_value.exists.return_value = True
        exists = self.redis_client.exists(key)
        self.assertTrue(exists)

    @patch('redis.StrictRedis')
    def test_incr(self, mock_strict_redis):
        key = "total_tests"
        mock_strict_redis.return_value.incr.return_value = 11
        result = self.redis_client.incr(key)
        self.assertEqual(result, 11)


if __name__ == '__main__':
    unittest.main()
