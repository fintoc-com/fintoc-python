"""Module to hold the invoices manager."""

from fintoc.mixins import ManagerMixin


class InvoicesManager(ManagerMixin):

    """Represents an invoices manager."""

    resource = "invoice"
    methods = ["all"]
