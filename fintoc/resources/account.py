from fintoc.managers import MovementsManager
from fintoc.mixins import ResourceMixin


class Account(ResourceMixin):

    """Represents a Fintoc Account."""

    def __init__(self, client_data, **kwargs):
        super().__init__(client_data, **kwargs)
        self._client_data = client_data
        self.__movements_manager = None

    @property
    def movements(self):
        if self.__movements_manager is None:
            self.__movements_manager = MovementsManager(
                f"/accounts/{self.id}/movements", self._client_data
            )
        return self.__movements_manager

    @movements.setter
    def movements(self, new_value):
        return
