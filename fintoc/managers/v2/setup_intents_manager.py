"""Module to hold the setup intents manager."""

from fintoc.mixins import ManagerMixin


class SetupIntentsManager(ManagerMixin):
    """Represents a setup intents manager."""

    resource = "setup_intent"
    methods = ["get"]
