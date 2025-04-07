from types import GeneratorType

import httpx
import pytest

from fintoc.client import Client


class TestClientCreationFunctionality:
    def setup_method(self):
        self.base_url = "https://test.com"
        self.api_key = "super_secret_api_key"
        self.user_agent = "fintoc-python/test"
        self.params = {"first_param": "first_value", "second_param": "second_value"}
        self.api_version = None

    def create_client(self, params=False, api_version=None):
        if not params:
            return Client(self.base_url, self.api_key, api_version, self.user_agent)

        return Client(
            self.base_url,
            self.api_key,
            self.api_version,
            self.user_agent,
            params=self.params,
        )

    def test_client_creation_without_params(self):
        client = self.create_client()
        assert isinstance(client, Client)
        assert client.base_url == self.base_url
        assert client.api_key == self.api_key
        assert client.user_agent == self.user_agent
        assert client.params == {}

    def test_client_creation_with_params(self):
        client = self.create_client(params=True)
        assert isinstance(client, Client)
        assert client.base_url == self.base_url
        assert client.api_key == self.api_key
        assert client.user_agent == self.user_agent
        assert client.params == self.params

    def test_client_headers_with_api_version(self):
        client = self.create_client(api_version="2023-01-01")
        assert isinstance(client.headers, dict)
        assert len(client.headers.keys()) == 3
        assert "Authorization" in client.headers
        assert "User-Agent" in client.headers
        assert client.headers["Authorization"] == self.api_key
        assert client.headers["User-Agent"] == self.user_agent
        assert client.headers["Fintoc-Version"] == "2023-01-01"

    def test_client_headers_without_api_version(self):
        client = self.create_client()
        assert isinstance(client.headers, dict)
        assert len(client.headers.keys()) == 2
        assert "Authorization" in client.headers
        assert "User-Agent" in client.headers
        assert client.headers["Authorization"] == self.api_key
        assert client.headers["User-Agent"] == self.user_agent

    def test_client_http_subclient_lazy_initialization(self):
        # pylint: disable=protected-access
        client = self.create_client()

        # Kind of a hack, but the test is necessary to test the internal client is None
        assert client._Client__client is None

        # Create an httpx client by calling the attribute
        assert isinstance(client._client, httpx.Client)

        # Now the internal client should exist
        assert isinstance(client._Client__client, httpx.Client)


class TestClientRequestFunctionality:
    @pytest.fixture(autouse=True)
    def patch_http_client(self, patch_http_client):
        pass

    def setup_method(self):
        self.base_url = "https://test.com"
        self.api_key = "super_secret_api_key"
        self.api_version = None
        self.user_agent = "fintoc-python/test"
        self.params = {"first_param": "first_value", "second_param": "second_value"}
        self.client = Client(
            self.base_url,
            self.api_key,
            self.api_version,
            self.user_agent,
            params=self.params,
        )

    def test_paginated_request(self):
        data = self.client.request("/movements", paginated=True)
        assert isinstance(data, GeneratorType)

    def test_get_request(self):
        data = self.client.request("/movements/3", method="get")
        assert isinstance(data, dict)
        assert len(data.keys()) > 0

    def test_delete_request(self):
        data = self.client.request("/movements/3", method="delete")
        assert isinstance(data, dict)
        assert len(data.keys()) == 0
