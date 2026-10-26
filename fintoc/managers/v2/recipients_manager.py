"""Module to hold the recipients manager."""

from fintoc.mixins import ManagerMixin


class RecipientsManager(ManagerMixin):
    """Represents a recipients manager."""

    resource = "recipient"
    methods = ["list", "get", "create", "update", "delete"]
