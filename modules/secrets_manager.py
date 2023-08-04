from config.config import Config
import boto3
from cachetools import TTLCache, cached
from typing import Any

# Global cache that stores up to 1000 items, and items expire after 1800 seconds (30 minutes)
cache = TTLCache(maxsize=1000, ttl=1800)


class SecretsManager:
    """
    This class handles fetching and caching secrets from AWS Parameter Store.
    """

    def __init__(self):
        """
        Initialize the SecretsManager.
        """
        self.ssm = boto3.client('ssm')
        self.config = Config()  # Instance of your SecretsConfig class

    @cached(cache=cache)
    def get_secret(self, key: str) -> Any:
        """
        Get a secret by its key. The secret is fetched from AWS Parameter Store
        the first time this method is called with a certain key, and then it's
        cached in memory for subsequent calls. The cache expires after 30 minutes.
        If the key is not in cache, it will try to get the value from the config.
        If the value in the config is a placeholder, it fetches the secret from AWS.

        :param key: The key of the secret.
        :return: The secret value.
        """
        try:
            # Split the key and access the corresponding attribute in the config
            attrs = key.split('.')
            val = self.config
            for attr in attrs:
                val = getattr(val, attr)

            # If the value is a placeholder, fetch the secret from AWS
            if isinstance(val, str) and val.startswith('{') and val.endswith('}'):
                param = self.ssm.get_parameter(Name=val[1:-1], WithDecryption=True)
                val = param['Parameter']['Value']

            return val

        except AttributeError:
            raise ValueError(f"No such key: {key}")

