from fintoc.managers import MovementsManager
from fintoc.mixins import ResourceMixin


class Account(ResourceMixin):

    """Represents a Fintoc Account."""

    def __init__(self, client, **kwargs):
        super().__init__(client, **kwargs)
        self._client = client
        self.__movements_manager = None

    @property
    def movements(self):
        if self.__movements_manager is None:
            self.__movements_manager = MovementsManager(
                f"/accounts/{self.id}/movements", self._client
            )
        return self.__movements_manager

    @movements.setter
    def movements(self, new_value):
        return
