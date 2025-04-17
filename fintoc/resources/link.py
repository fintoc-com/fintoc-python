"""Module to hold the Link resource."""

from fintoc.managers import (
    AccountsManager,
    InvoicesManager,
    RefreshIntentsManager,
    SubscriptionsManager,
    TaxReturnsManager,
)
from fintoc.mixins import ResourceMixin


class Link(ResourceMixin):

    """Represents a Fintoc Link."""

    resource_identifier = "_link_token"

    def __init__(self, client, handlers, methods, path, **kwargs):
        super().__init__(client, handlers, methods, path, **kwargs)
        self.__accounts_manager = None
        self.__subscriptions_manager = None
        self.__tax_returns_manager = None
        self.__invoices_manager = None
        self.__refresh_intents_manager = None

    @property
    def accounts(self):
        """Proxies the accounts manager."""
        if self.__accounts_manager is None:
            self.__accounts_manager = AccountsManager("/v1/accounts", self._client)
        return self.__accounts_manager

    @accounts.setter
    def accounts(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")

    @property
    def subscriptions(self):
        # TODO: this method should be deprecated as it's no longer allowed
        # in our API
        """Proxies the subscriptions manager."""
        if self.__subscriptions_manager is None:
            self.__subscriptions_manager = SubscriptionsManager(
                "/v1/subscriptions", self._client
            )
        return self.__subscriptions_manager

    @subscriptions.setter
    def subscriptions(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")

    @property
    def tax_returns(self):
        """Proxies the tax_returns manager."""
        if self.__tax_returns_manager is None:
            self.__tax_returns_manager = TaxReturnsManager(
                "/v1/tax_returns", self._client
            )
        return self.__tax_returns_manager

    @tax_returns.setter
    def tax_returns(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")

    @property
    def invoices(self):
        """Proxies the invoices manager."""
        if self.__invoices_manager is None:
            self.__invoices_manager = InvoicesManager("/v1/invoices", self._client)
        return self.__invoices_manager

    @invoices.setter
    def invoices(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")

    @property
    def refresh_intents(self):
        """Proxies the refresh_intents manager."""
        if self.__refresh_intents_manager is None:
            self.__refresh_intents_manager = RefreshIntentsManager(
                "/v1/refresh_intents", self._client
            )
        return self.__refresh_intents_manager

    @refresh_intents.setter
    def refresh_intents(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")
