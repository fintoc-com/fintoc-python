"""Module to hold the crossborder transfers manager."""

from fintoc.mixins import ManagerMixin


class CrossborderTransfersManager(ManagerMixin):
    """Represents a crossborder transfers manager."""

    resource = "crossborder_transfer"
    methods = ["list", "get", "create"]
