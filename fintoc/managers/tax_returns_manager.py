"""Module to hold the tax_returns manager."""

from fintoc.mixins import ManagerMixin


class TaxRetunsManager(ManagerMixin):

    """Represents a tax_returns manager."""

    resource = "tax_return"
    methods = ["all", "get"]
