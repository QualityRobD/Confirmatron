import os
import redis
import uuid


class RedisClient:
    def __init__(self):

        # Get Redis host and port from environment variables or Kubernetes secrets
        _redis_host = os.environ.get("REDIS_HOST", "localhost")  # Replace "localhost" with the default Redis host if needed
        _redis_port = int(os.environ.get("REDIS_PORT", 6379))  # Replace 6379 with the default Redis port if needed

        # Create the Redis client with the obtained host and port
        self.redis_client = redis.StrictRedis(host=_redis_host, port=_redis_port, db=0)

    def create_key(self, api_name: str, expire_seconds: int = 7200):
        unique_id = str(uuid.uuid4())
        key = f"{api_name}:{unique_id}"
        self.redis_client.setex(key, expire_seconds, "")
        return key

    def retrieve_results(self, key: str):
        return self.redis_client.hgetall(key)

    def store_result(self, key: str, result):
        self.redis_client.hset(key, '', result)

    def get_redis_keys(self, api_name: str):
        all_keys = self.redis_client.keys(f"{api_name}:*")
        return [key.decode("utf-8") for key in all_keys]

    def exists(self, key):
        return self.redis_client.exists(key)
