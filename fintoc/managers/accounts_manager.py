"""Module to hold the accounts manager."""

from fintoc.mixins import ManagerMixin


class AccountsManager(ManagerMixin):

    """Represents an accounts manager."""

    resource = "account"
    methods = ["all", "get"]
