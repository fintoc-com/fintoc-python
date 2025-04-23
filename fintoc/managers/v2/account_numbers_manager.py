"""Module to hold the account numbers manager."""

from fintoc.mixins import ManagerMixin


class AccountNumbersManager(ManagerMixin):
    """Represents an account numbers manager."""

    resource = "account_number"
    methods = ["list", "get", "update", "create"]
