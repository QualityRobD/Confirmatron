from flask import current_app
import boto3
from cachetools import TTLCache, cached
from functools import cached_property
from typing import Any
from dotenv import load_dotenv
import os
from config.config import Config, Api

# Global cache that stores up to 1000 items, and items expire after 1800 seconds (30 minutes)
cache = TTLCache(maxsize=1000, ttl=1800)


class SingletonMeta(type):
    """
    This is a metaclass that implements the Singleton design pattern.
    A Singleton class is a class that is instantiated only once;
    subsequent calls to instantiate it actually return the same instance.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        This method is called when the class is "called" (i.e., instantiated).
        It checks if an instance of the class has already been created.
        If so, it returns the existing instance. If not, it creates a new instance and stores it.

        :param args: Positional arguments to be passed to the class constructor.
        :param kwargs: Keyword arguments to be passed to the class constructor.
        :return: An instance of the class.
        """

        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SecretsManager(metaclass=SingletonMeta):
    """
    This class handles fetching and caching secrets from AWS Parameter Store.
    """

    def __init__(self):
        """
        Initialize the SecretsManager.
        """
        self._ssm = None

    @cached_property
    def ssm(self):
        """
        Lazily load and cache the SSM client.
        """
        return boto3.client('ssm')

    @cached(cache=cache)
    def get_secret(self, key: str, api_name: str = None) -> Any:
        config: Config = current_app.config['config']

        """
        Get a secret by its key. The secret is fetched from AWS Parameter Store
        the first time this method is called with a certain key, and then it's
        cached in memory for subsequent calls. The cache expires after 30 minutes.
        If the key is not in cache, it will try to get the value from the config.
        If the value in the config is a placeholder, it fetches the secret from AWS
        or .env file depending on the RUN_ENV environment variable.

        :param key: The key of the secret, corresponding to an attribute in the Config class.
        :return: The secret value.
        :raises ValueError: If the key does not match any attribute in the Config class.
        """
        try:
            if api_name:
                config = config.test_apis.apis.get("apiOne")

            val = getattr(config, key)  # Directly get the attribute from the config

            # If the value is a placeholder, check the environment
            if isinstance(val, str) and val.startswith('{') and val.endswith('}'):
                run_env = os.getenv('RUN_ENV')

                if run_env == 'LOCAL':
                    load_dotenv()  # load environment variables from .env file
                    val = os.getenv(val[1:-1])
                else:
                    # fetch the secret from AWS
                    param = self.ssm.get_parameter(Name=val[1:-1], WithDecryption=True)
                    val = param['Parameter']['Value']

            return val

        except AttributeError:
            raise ValueError(f"No such key: {key}")

    @staticmethod
    def load_api_config(api_name: str) -> 'Api':
        """
        Load the API configuration from the current Flask application's configuration.

        This method retrieves the API configuration based on the provided API name
        from the 'test_apis' object in the Flask application's configuration.

        :param api_name: The name of the API whose configuration needs to be loaded.
        :return: An Api object that contains the configuration for the specified API.
        """
        return current_app.config['config'].test_apis.apis.get(api_name)


    @staticmethod
    def clear_cache():
        """
        Clears all cached secrets. Useful when the secrets in the AWS Parameter Store
        have been updated and the application needs to access the new values immediately.
        """
        cache.clear()

    @classmethod
    def api_context(cls, api_name: str) -> '_ApiContextManager':
        """
        Class method that provides a context manager for using API secrets.
        Within this context, the API secrets are accessible as properties
        of the 'config' object returned by this method.

        :param api_name: The name of the API for which to load secrets.
        :return: A context manager that yields an Api object.
        """
        return _ApiContextManager(SecretsManager(), api_name)


class _ApiContextManager:
    def __init__(self, secrets_manager: SecretsManager, api_name: str):
        """
        Initialize an ApiControllerContext.

        :param secrets_manager: The SecretsManager to use for loading and getting secrets.
        :param api_name: The name of the API for this context.
        """
        self._secrets_manager = secrets_manager
        self._config = current_app.config['config']
        self.api = current_app.config['config'].test_apis.apis.get(api_name, None)

    def __enter__(self):
        """
        Enter the API context. Loads the secrets for the API and sets up the API attributes.

        :return: The API context.
        """
        if not self.api:
            raise ValueError(f"No such API: {self.api.api_name}")

        # Load the secrets
        self._secrets_manager.load_api_config(self.api.api_name)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the API context. Invalidates the cache to remove the secrets from memory.

        :param exc_type: The type of exception that caused the context to be exited, if any.
        :param exc_val: The instance of the exception that caused the context to be exited, if any.
        :param exc_tb: The traceback of the exception that caused the context to be exited, if any.
        """
        # removes the config from memory
        self._config = None

    def get_secret(self, key: str) -> Any:
        """
        Get a secret for this API.

        :param key: The key of the secret.
        :return: The secret value.
        """
        # Get a secret for this API
        return self._secrets_manager.get_secret(f"{self.api.api_name}.{key}")
