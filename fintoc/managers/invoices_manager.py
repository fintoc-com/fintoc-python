"""Module to hold the invoices manager."""

from fintoc.managers._link_token_manager import LinkTokenManager


class InvoicesManager(LinkTokenManager):

    """Represents an invoices manager."""

    resource = "invoice"
    methods = ["all"]
