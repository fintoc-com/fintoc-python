from fintoc.managers import AccountsManager, SubscriptionsManager, TaxRetunsManager
from fintoc.mixins import ResourceMixin


class Link(ResourceMixin):

    """Represents a Fintoc Link."""

    def __init__(self, client, handlers, methods, path, **kwargs):
        super().__init__(client, handlers, methods, path, **kwargs)
        self.__accounts_manager = None
        self.__subscriptions_manager = None
        self.__tax_returns_manager = None
        self.__invoices_manager = None

    @property
    def accounts(self):
        if self.__accounts_manager is None:
            self.__accounts_manager = AccountsManager("/accounts", self._client)
        return self.__accounts_manager

    @accounts.setter
    def accounts(self, new_value):
        return

    @property
    def subscriptions(self):
        if self.__subscriptions_manager is None:
            self.__subscriptions_manager = SubscriptionsManager(
                "/subscriptions", self._client
            )
        return self.__subscriptions_manager

    @subscriptions.setter
    def subscriptions(self, new_value):
        return

    @property
    def tax_returns(self):
        if self.__tax_returns_manager is None:
            self.__tax_returns_manager = TaxRetunsManager("/tax_returns", self._client)
        return self.__tax_returns_manager

    @tax_returns.setter
    def tax_returns(self, new_value):
        return

    @property
    def invoices(self):
        if self.__invoices_manager is None:
            self.__invoices_manager = TaxRetunsManager("/invoices", self._client)
        return self.__invoices_manager

    @invoices.setter
    def invoices(self, new_value):
        return
