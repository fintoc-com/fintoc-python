"""Module to hold the payouts manager."""

from fintoc.managers.payout_resources_manager import PayoutResourcesManager
from fintoc.mixins import ManagerMixin


class PayoutsManager(ManagerMixin):

    """Represents a payouts manager."""

    resource = "payout"
    methods = ["list", "get"]

    def __init__(self, path, client):
        super().__init__(path, client)
        self.__resources_manager = None

    @property
    def resources(self):
        """Proxies the payout resources manager."""
        if self.__resources_manager is None:
            self.__resources_manager = PayoutResourcesManager(
                "/v1/payouts/{payout_id}/resources",
                self._client,
            )
        return self.__resources_manager

    @resources.setter
    def resources(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")
