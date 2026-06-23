"""Module to hold the subscriptions manager."""

from fintoc.managers.v2.subscription_items_manager import SubscriptionItemsManager
from fintoc.mixins import ManagerMixin


class SubscriptionsManager(ManagerMixin):
    """Represents a subscriptions manager."""

    resource = "subscription"
    methods = ["list", "get", "create", "update", "cancel"]

    def __init__(self, path, client):
        super().__init__(path, client)
        self.__items_manager = None

    @property
    def items(self):
        """Proxies the subscription items manager."""
        if self.__items_manager is None:
            self.__items_manager = SubscriptionItemsManager(
                "/v2/subscriptions/{subscription_id}/items",
                self._client,
            )
        return self.__items_manager

    @items.setter
    def items(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")

    def _cancel(self, identifier, **kwargs):
        """Cancel a subscription."""
        path = f"{self._build_path(**kwargs)}/{identifier}/cancel"
        return self._create(path_=path, **kwargs)
