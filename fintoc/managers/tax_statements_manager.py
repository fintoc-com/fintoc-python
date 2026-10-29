"""Module to hold the tax_statements manager."""

from fintoc.mixins import ManagerMixin


class TaxStatementsManager(ManagerMixin):

    """Represents a tax_statements manager."""

    resource = "tax_statement"
    methods = ["list", "get"]
