# pylint: disable=duplicate-code
"""Module to hold the accounts manager."""

from fintoc.managers.v2.account_statements_manager import AccountStatementsManager
from fintoc.managers.v2.movements_manager import MovementsManager
from fintoc.mixins import ManagerMixin


class AccountsManager(ManagerMixin):
    """Represents an accounts manager."""

    resource = "account"
    methods = ["list", "get", "create", "update"]

    def __init__(self, path, client):
        super().__init__(path, client)
        self.__account_statements_manager = None
        self.__movements_manager = None

    @property
    def account_statements(self):
        """Proxies the account statements manager."""
        if self.__account_statements_manager is None:
            self.__account_statements_manager = AccountStatementsManager(
                "/v2/accounts/{account_id}/account_statements",
                self._client,
            )
        return self.__account_statements_manager

    @account_statements.setter
    def account_statements(self, new_value):
        raise NameError("Attribute name corresponds to a manager")

    @property
    def movements(self):
        """Proxies the movements manager."""
        if self.__movements_manager is None:
            self.__movements_manager = MovementsManager(
                "/v2/accounts/{account_id}/movements",
                self._client,
            )
        return self.__movements_manager

    @movements.setter
    def movements(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")
