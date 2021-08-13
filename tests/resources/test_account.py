import pytest

from fintoc.client import Client
from fintoc.mixins import ManagerMixin
from fintoc.resources import Account


class TestAccountResource:
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
        self.path = "/accounts"
        self.handlers = {
            "update": lambda object_, identifier: object_,
            "delete": lambda identifier: identifier,
        }

    def test_movements_manager(self):
        # pylint: disable=protected-access
        account = Account(self.client, self.handlers, [], self.path, **{"id": "idx"})

        assert account._Account__movements_manager is None
        assert isinstance(account.movements, ManagerMixin)
        assert account._Account__movements_manager is not None
        assert isinstance(account._Account__movements_manager, ManagerMixin)

        with pytest.raises(NameError):
            account.movements = None

        assert account.movements is not None
        assert isinstance(account.movements, ManagerMixin)
        assert isinstance(account._Account__movements_manager, ManagerMixin)
