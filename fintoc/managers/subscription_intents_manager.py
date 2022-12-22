"""Module to hold the subscription_intents manager."""

from fintoc.mixins import ManagerMixin


class SubscriptionIntentsManager(ManagerMixin):

    """Represents a subscription_intents manager."""

    resource = "subscription_intent"
    methods = ["all", "get", "create"]
