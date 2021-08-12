"""Module to hold the subscriptions manager."""

from fintoc.mixins import ManagerMixin


class SubscriptionsManager(ManagerMixin):

    """Represents a subscriptions manager."""

    resource = "subscription"
    methods = ["all", "get"]
