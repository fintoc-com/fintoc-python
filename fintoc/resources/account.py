"""Module to hold the Account resource."""

from fintoc.managers import MovementsManager
from fintoc.mixins import ResourceMixin


class Account(ResourceMixin):

    """Represents a Fintoc Account."""

    def __init__(self, client, handlers, methods, path, **kwargs):
        super().__init__(client, handlers, methods, path, **kwargs)
        self.__movements_manager = None
        self._link_token = None

    @property
    def movements(self):
        """Proxies the movements manager."""
        if self.__movements_manager is None:
            self.__movements_manager = MovementsManager(
                f"/accounts/{self.id}/movements",
                self._client,
                link_token=self._link_token
            )
        return self.__movements_manager

    @movements.setter
    def movements(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")
