"""Module to hold the account verification manager."""

from fintoc.mixins import ManagerMixin


class AccountVerificationsManager(ManagerMixin):
    """Represents an account verification manager."""

    resource = "account_verification"
    methods = ["list", "get", "create"]
