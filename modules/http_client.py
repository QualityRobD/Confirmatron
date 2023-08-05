import requests
from requests.exceptions import RequestException
from typing import Dict, Optional

class HttpClient:
    """
    Simple HTTP client for making requests.
    """

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, path: str, params: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Makes a GET request to the specified path.

        :param path: The path to make the GET request to.
        :param params: Optional dictionary of query parameters.
        :returns: A requests.Response object.
        :raises RequestException: If the request fails for any reason.
        """
        try:
            response = requests.get(f"{self.base_url}/{path}", params=params)
            response.raise_for_status()
        except RequestException as e:
            # handle or raise the exception as needed
            raise e
        return response

    def post(self, path: str, data: Optional[Dict] = None) -> requests.Response:
        """
        Makes a POST request to the specified path.

        :param path: The path to make the POST request to.
        :param data: Optional dictionary of data to send in the request body.
        :returns: A requests.Response object.
        :raises RequestException: If the request fails for any reason.
        """
        try:
            response = requests.post(f"{self.base_url}/{path}", json=data)
            response.raise_for_status()
        except RequestException as e:
            # handle or raise the exception as needed
            raise e
        return response

    # ... similar methods for put, delete, etc ...

    def put(self, path: str, data: Optional[Dict] = None) -> requests.Response:
        """
        Makes a PUT request to the specified path.

        :param path: The path to make the PUT request to.
        :param data: Optional dictionary of data to send in the request body.
        :returns: A requests.Response object.
        :raises RequestException: If the request fails for any reason.
        """
        try:
            response = requests.put(f"{self.base_url}/{path}", json=data)
            response.raise_for_status()
        except RequestException as e:
            # handle or raise the exception as needed
            raise e
        return response

    def delete(self, path: str) -> requests.Response:
        """
        Makes a DELETE request to the specified path.

        :param path: The path to make the DELETE request to.
        :returns: A requests.Response object.
        :raises RequestException: If the request fails for any reason.
        """
        try:
            response = requests.delete(f"{self.base_url}/{path}")
            response.raise_for_status()
        except RequestException as e:
            # handle or raise the exception as needed
            raise e
        return response
