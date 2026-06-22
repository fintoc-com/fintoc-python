"""Module to hold the entities manager."""

from fintoc.managers.v2.onboardings_manager import OnboardingsManager
from fintoc.mixins import ManagerMixin


class EntitiesManager(ManagerMixin):
    """Represents an entities manager."""

    resource = "entity"
    methods = ["list", "get", "create"]

    def __init__(self, path, client):
        super().__init__(path, client)
        self.__onboardings_manager = None

    @property
    def onboardings(self):
        """Proxies the onboardings manager."""
        if self.__onboardings_manager is None:
            self.__onboardings_manager = OnboardingsManager(
                "/v2/entities/{entity_id}/onboardings",
                self._client,
            )
        return self.__onboardings_manager

    @onboardings.setter
    def onboardings(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")
