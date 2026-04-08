# pylint: disable=duplicate-code
"""Module to hold the account statements manager."""

from fintoc.mixins import ManagerMixin


class AccountStatementsManager(ManagerMixin):
    """Represents an account statements manager."""

    resource = "account_statement"
    methods = ["list"]
