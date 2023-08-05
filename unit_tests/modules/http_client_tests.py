import pytest
import requests_mock
from modules.http_client import HttpClient


@pytest.fixture
def http_client():
    return HttpClient()


@pytest.fixture
def req_mock():
    with requests_mock.Mocker() as m:
        yield m


def test_get(http_client, req_mock):
    url = 'http://test.com'
    expected = {"success": True}
    req_mock.get(url, json=expected)

    response = http_client.get(url)
    assert response == expected


def test_post(http_client, req_mock):
    url = 'http://test.com'
    data = {"key": "value"}
    expected = {"success": True}
    req_mock.post(url, json=expected)

    response = http_client.post(url, data)
    assert response == expected


def test_put(http_client, req_mock):
    url = 'http://test.com'
    data = {"key": "value"}
    expected = {"success": True}
    req_mock.put(url, json=expected)

    response = http_client.put(url, data)
    assert response == expected


def test_delete(http_client, req_mock):
    url = 'http://test.com'
    expected = {"success": True}
    req_mock.delete(url, json=expected)

    response = http_client.delete(url)
    assert response == expected
