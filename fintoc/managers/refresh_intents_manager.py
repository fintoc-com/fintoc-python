"""Module to hold the refresh_intents manager."""

from fintoc.mixins import ManagerMixin


class RefreshIntentsManager(ManagerMixin):

    """Represents a refresh_intents manager."""

    resource = "refresh_intent"
    methods = ["all", "get", "create"]
