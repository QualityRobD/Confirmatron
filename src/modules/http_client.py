import requests
from requests.exceptions import RequestException
from typing import Dict, Optional, Any
from modules.constants import Environments
from modules.auth_0_handler import Auth0Handler


class HttpClient:
    """
    Simple HTTP client for making requests.
    """

    def __init__(self, base_url: str, environment_under_test: Environments):
        self.base_url = base_url
        auth = Auth0Handler()

        bearer_token_fetchers = {
            Environments.TEST: auth.get_test_token,
            Environments.BETA: auth.get_beta_token,
            Environments.PROD: auth.get_prod_token,
        }
        fetcher = bearer_token_fetchers.get(environment_under_test)
        if fetcher is not None:
            self.bearer_token = fetcher()

        self.session = requests.Session()

    def get(self,
            path: str,
            params: Optional[Dict[str, str]] = None,
            extra_headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Makes a GET request to the specified path.

        :param path: The path to make the GET request to.
        :param params: Optional dictionary of query parameters.
        :param extra_headers: Optional dictionary of headers to be added to the request.
        :returns: A requests.Response object.
        :raises RequestException: If the request fails for any reason.
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        if extra_headers:
            headers.update(extra_headers)

        try:
            response = requests.get(f"{self.base_url}/{path}", headers=headers, params=params)
            response.raise_for_status()
        except RequestException as e:
            # handle or raise the exception as needed
            raise e
        return response

    def post(self,
             path: str,
             data: Optional[Dict[str, Any]] = None,
             extra_headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Makes a POST request to the specified path.

        :param path: The path to make the POST request to.
        :param data: Optional dictionary of data to send as JSON in the body of the request.
        :param extra_headers: Optional dictionary of headers to be added to the request.
        :returns: A requests.Response object.
        :raises RequestException: If the request fails for any reason.
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        if extra_headers:
            headers.update(extra_headers)

        try:
            response = requests.post(f"{self.base_url}/{path}", headers=headers, json=data)
            response.raise_for_status()
        except RequestException as e:
            # handle or raise the exception as needed
            raise e
        return response

    def put(self,
            path: str,
            data: Optional[Dict[str, Any]] = None,
            extra_headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Makes a PUT request to the specified path.

        :param path: The path to make the PUT request to.
        :param data: Optional dictionary of data to send as JSON in the body of the request.
        :param extra_headers: Optional dictionary of headers to be added to the request.
        :returns: A requests.Response object.
        :raises RequestException: If the request fails for any reason.
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        if extra_headers:
            headers.update(extra_headers)

        try:
            response = requests.put(f"{self.base_url}/{path}", headers=headers, json=data)
            response.raise_for_status()
        except RequestException as e:
            # handle or raise the exception as needed
            raise e
        return response

    def delete(self,
               path: str,
               params: Optional[Dict[str, str]] = None,
               extra_headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Makes a DELETE request to the specified path.

        :param path: The path to make the DELETE request to.
        :param params: Optional dictionary of query parameters.
        :param extra_headers: Optional dictionary of headers to be added to the request.
        :returns: A requests.Response object.
        :raises RequestException: If the request fails for any reason.
        """
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        if extra_headers:
            headers.update(extra_headers)

        try:
            response = requests.delete(f"{self.base_url}/{path}", headers=headers, params=params)
            response.raise_for_status()
        except RequestException as e:
            # handle or raise the exception as needed
            raise e
        return response

