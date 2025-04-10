import pytest

from fintoc.client import Client
from fintoc.managers import AccountsManager


class TestAccountsManagerHandlers:
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
        self._link_token = "link_token"
        self.path = "/accounts"
        self.manager = AccountsManager(
            self.path, self.client, link_token=self._link_token
        )

    def test_post_get_handler(self):
        # pylint: disable=protected-access
        id_ = "idx"
        object_ = self.manager.get(id_)
        assert object_._link_token is not None

    def test_post_all_handler_list(self):
        # pylint: disable=protected-access
        objects = self.manager.all(lazy=False)
        assert isinstance(objects, list)
        for obj in objects:
            assert obj._link_token is not None

    def test_post_all_handler_generator(self):
        # pylint: disable=protected-access
        objects = self.manager.all()
        assert not isinstance(objects, list)
        for obj in objects:
            assert obj._link_token is not None
