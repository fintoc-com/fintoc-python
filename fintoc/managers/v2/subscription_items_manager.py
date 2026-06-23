"""Module to hold the subscription items manager."""

from fintoc.mixins import ManagerMixin


class SubscriptionItemsManager(ManagerMixin):
    """Represents a subscription items manager."""

    resource = "subscription_item"
    methods = ["create", "update"]
