"""Module to hold the crossborder quotes manager."""

from fintoc.mixins import ManagerMixin


class CrossborderQuotesManager(ManagerMixin):
    """Represents a crossborder quotes manager."""

    resource = "crossborder_quote"
    methods = ["get", "create"]
