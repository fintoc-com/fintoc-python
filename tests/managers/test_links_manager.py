import pytest

from fintoc.client import Client
from fintoc.managers import LinksManager


class TestLinksManagerHandlers:
    @pytest.fixture(autouse=True)
    def patch_http_client(self, patch_http_client):
        pass

    def setup_method(self):
        self.base_url = "https://test.com"
        self.api_key = "super_secret_api_key"
        self.user_agent = "fintoc-python/test"
        self.params = {"first_param": "first_value", "second_param": "second_value"}
        self.client = Client(
            self.base_url,
            self.api_key,
            self.user_agent,
            params=self.params,
        )
        self.path = "/links"
        self.manager = LinksManager(self.path, self.client)

    def test_post_get_handler(self):
        # pylint: disable=protected-access
        id_ = "idx"
        object_ = self.manager.get(id_)
        assert object_._client is not self.manager._client
        assert "link_token" not in self.manager._client.params
        assert "link_token" in object_._client.params

    def test_post_update_handler(self):
        # pylint: disable=protected-access
        id_ = "idx"
        object_ = self.manager.update(id_)
        assert object_._client is not self.manager._client
        assert "link_token" not in self.manager._client.params
        assert "link_token" in object_._client.params
