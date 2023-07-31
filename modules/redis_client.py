import os
import redis


class RedisClient:
    def __init__(self):

        # Get Redis host and port from environment variables or Kubernetes secrets
        _redis_host = os.environ.get("REDIS_HOST", "localhost")  # Replace "localhost" with the default Redis host if needed
        _redis_port = int(os.environ.get("REDIS_PORT", 6379))  # Replace 6379 with the default Redis port if needed

        # Create the Redis client with the obtained host and port
        self.redis_client = redis.StrictRedis(host=_redis_host, port=_redis_port, db=0)

    def retrieve_results(self, redis_key: str):
        return self.redis_client.lrange(redis_key, 0, -1)

    def store_result(self, redis_key: str, result):
        self.redis_client.rpush(redis_key, result)

    def get_redis_keys(self, api_name: str):
        all_keys = self.redis_client.keys(f"{api_name}:*")
        return [key.decode("utf-8") for key in all_keys]
