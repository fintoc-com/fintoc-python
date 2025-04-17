"""Module to hold the accounts manager."""

from fintoc.managers.movements_manager import MovementsManager
from fintoc.mixins import ManagerMixin


# pylint: disable=duplicate-code
class AccountsManager(ManagerMixin):

    """Represents an accounts manager."""

    resource = "account"
    methods = ["list", "get"]

    def __init__(self, path, client):
        super().__init__(path, client)
        self.__movements_manager = None

    @property
    def movements(self):
        """Proxies the movements manager."""
        if self.__movements_manager is None:
            self.__movements_manager = MovementsManager(
                "/v1/accounts/{account_id}/movements",
                self._client,
            )
        return self.__movements_manager

    @movements.setter
    def movements(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")
