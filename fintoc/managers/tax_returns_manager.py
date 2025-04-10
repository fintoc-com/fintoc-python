"""Module to hold the tax_returns manager."""

from fintoc.managers._link_token_manager import LinkTokenManager


class TaxReturnsManager(LinkTokenManager):

    """Represents a tax_returns manager."""

    resource = "tax_return"
    methods = ["all", "get"]
