import pytest

from fintoc.client import Client
from fintoc.mixins import ManagerMixin
from fintoc.resources import Link


class TestLinkResource:
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
        self.handlers = {
            "update": lambda object_, identifier: object_,
            "delete": lambda identifier: identifier,
        }

    def test_accounts_manager(self):
        # pylint: disable=protected-access
        link = Link(self.client, self.handlers, [], self.path, **{})

        assert link._Link__accounts_manager is None
        assert isinstance(link.accounts, ManagerMixin)
        assert link._Link__accounts_manager is not None
        assert isinstance(link._Link__accounts_manager, ManagerMixin)

        with pytest.raises(NameError):
            link.accounts = None

        assert link.accounts is not None
        assert isinstance(link.accounts, ManagerMixin)
        assert isinstance(link._Link__accounts_manager, ManagerMixin)

    def test_subscriptions_manager(self):
        # pylint: disable=protected-access
        link = Link(self.client, self.handlers, [], self.path, **{})

        assert link._Link__subscriptions_manager is None
        assert isinstance(link.subscriptions, ManagerMixin)
        assert link._Link__subscriptions_manager is not None
        assert isinstance(link._Link__subscriptions_manager, ManagerMixin)

        with pytest.raises(NameError):
            link.subscriptions = None

        assert link.subscriptions is not None
        assert isinstance(link.subscriptions, ManagerMixin)
        assert isinstance(link._Link__subscriptions_manager, ManagerMixin)

    def test_tax_returns_manager(self):
        # pylint: disable=protected-access
        link = Link(self.client, self.handlers, [], self.path, **{})

        assert link._Link__tax_returns_manager is None
        assert isinstance(link.tax_returns, ManagerMixin)
        assert link._Link__tax_returns_manager is not None
        assert isinstance(link._Link__tax_returns_manager, ManagerMixin)

        with pytest.raises(NameError):
            link.tax_returns = None

        assert link.tax_returns is not None
        assert isinstance(link.tax_returns, ManagerMixin)
        assert isinstance(link._Link__tax_returns_manager, ManagerMixin)

    def test_invoices_manager(self):
        # pylint: disable=protected-access
        link = Link(self.client, self.handlers, [], self.path, **{})

        assert link._Link__invoices_manager is None
        assert isinstance(link.invoices, ManagerMixin)
        assert link._Link__invoices_manager is not None
        assert isinstance(link._Link__invoices_manager, ManagerMixin)

        with pytest.raises(NameError):
            link.invoices = None

        assert link.invoices is not None
        assert isinstance(link.invoices, ManagerMixin)
        assert isinstance(link._Link__invoices_manager, ManagerMixin)

    def test_refresh_intents_manager(self):
        # pylint: disable=protected-access
        link = Link(self.client, self.handlers, [], self.path, **{})

        assert link._Link__refresh_intents_manager is None
        assert isinstance(link.refresh_intents, ManagerMixin)
        assert link._Link__refresh_intents_manager is not None
        assert isinstance(link._Link__refresh_intents_manager, ManagerMixin)

        with pytest.raises(NameError):
            link.refresh_intents = None

        assert link.refresh_intents is not None
        assert isinstance(link.refresh_intents, ManagerMixin)
        assert isinstance(link._Link__refresh_intents_manager, ManagerMixin)
