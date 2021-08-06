from fintoc.managers import AccountsManager, SubscriptionsManager
from fintoc.mixins import ResourceMixin


class Link(ResourceMixin):

    """Represents a Fintoc Link."""

    def __init__(self, client_data, **kwargs):
        super().__init__(client_data, **kwargs)
        self._client_data = client_data
        self.__accounts_manager = None
        self.__subscriptions_manager = None

    @property
    def accounts(self):
        if self.__accounts_manager is None:
            self.__accounts_manager = AccountsManager("/accounts", self._client_data)
        return self.__accounts_manager

    @accounts.setter
    def accounts(self, new_value):
        return

    @property
    def subscriptions(self):
        if self.__subscriptions_manager is None:
            self.__subscriptions_manager = SubscriptionsManager(
                "/subscriptions", self._client_data
            )
        return self.__subscriptions_manager

    @subscriptions.setter
    def subscriptions(self, new_value):
        return
