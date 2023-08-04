from config.config import Config
import boto3
from cachetools import TTLCache, cached
from typing import Any
from dotenv import load_dotenv
import os

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
        If the environment variable 'RUN_ENV' is set to 'LOCAL', it will use python-dotenv to fetch secrets.

        :param key: The key of the secret.
        :return: The secret value.
        """
        try:
            # Split the key and access the corresponding attribute in the config
            attrs = key.split('.')
            val = self.config
            for attr in attrs:
                val = getattr(val, attr)

            # If the value is a placeholder, check the environment
            if isinstance(val, str) and val.startswith('{') and val.endswith('}'):
                run_env = os.getenv('RUN_ENV')

                # If running locally, use python-dotenv
                if run_env == 'LOCAL':
                    load_dotenv()  # load environment variables from .env file
                    val = os.getenv(val[1:-1])
                else:
                    # Otherwise, fetch the secret from AWS
                    param = self.ssm.get_parameter(Name=val[1:-1], WithDecryption=True)
                    val = param['Parameter']['Value']

            return val

        except AttributeError:
            raise ValueError(f"No such key: {key}")

