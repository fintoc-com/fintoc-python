"""Module to hold the link intents manager."""

from fintoc.mixins import ManagerMixin


class LinkIntentsManager(ManagerMixin):

    """Represents a link intents manager."""

    resource = "link_intent"
    methods = ["create"]
