"""Module to hold the transfers manager."""

from fintoc.mixins import ManagerMixin


class TransfersManager(ManagerMixin):
    """Represents a transfers manager."""

    resource = "transfer"
    methods = ["list", "get", "create"]
