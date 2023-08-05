import requests
from cachetools import TTLCache, cached
from typing import Optional
from modules.secrets_manager import SecretsManager

# Global cache for Auth0 credentials
# stores up to 3 items (one per environment), each expires after 1800 seconds (30 minutes)
auth0_cache = TTLCache(maxsize=3, ttl=1800)


class Auth0Handler:
    """
    This class handles authentication with Auth0 for multiple environments.
    """

    def __init__(self, secrets_manager: SecretsManager):
        """
        Initialize the Auth0Handler.

        :param secrets_manager: An instance of SecretsManager.
        """
        self.secrets_manager = secrets_manager

    def _get_auth0_token(self, env: str) -> Optional[str]:
        """
        Helper method to get an Auth0 token for a specific environment. The token is fetched from Auth0 the first time
        this method is called for a certain environment, and then it's cached in memory for subsequent calls.
        The cache expires after 30 minutes.

        :param env: The environment for which to get the token. Should be 'test', 'beta', or 'prod'.
        :return: The Auth0 token for the specified environment.
        """
        auth_url = self.secrets_manager.get_secret(f'confirmatron.auth_zero.{env}.auth_url')
        client_id = self.secrets_manager.get_secret(f'confirmatron.auth_zero.{env}.client_id')
        client_secret = self.secrets_manager.get_secret(f'confirmatron.auth_zero.{env}.client_secret')
        audience = self.secrets_manager.get_secret(f'confirmatron.auth_zero.{env}.audience')
        grant_type = self.secrets_manager.get_secret(f'confirmatron.auth_zero.{env}.grant_type')

        headers = {'content-type': 'application/json'}
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "audience": audience,
            "grant_type": grant_type
        }

        response = requests.post(auth_url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception if the request failed
        token = response.json().get('access_token')

        return token

    @cached(cache=auth0_cache)
    def get_test_token(self) -> Optional[str]:
        """
        Get an Auth0 token for the test environment.

        :return: The Auth0 token for the test environment.
        """
        return self._get_auth0_token('test')

    @cached(cache=auth0_cache)
    def get_beta_token(self) -> Optional[str]:
        """
        Get an Auth0 token for the beta environment.

        :return: The Auth0 token for the beta environment.
        """
        return self._get_auth0_token('beta')

    @cached(cache=auth0_cache)
    def get_prod_token(self) -> Optional[str]:
        """
        Get an Auth0 token for the prod environment.

        :return: The Auth0 token for the prod environment.
        """
        return self._get_auth0_token('prod')
