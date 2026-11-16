"""Module to hold the crossborder transfers manager."""

from fintoc.mixins import ManagerMixin


class CrossborderTransfersManager(ManagerMixin):
    """Represents a crossborder transfers manager."""

    resource = "crossborder_transfer"
    methods = ["list", "get", "create", "cancel", "simulate_credit"]

    def _cancel(self, identifier, **kwargs):
        """Cancel a crossborder transfer."""
        path = f"{self._build_path(**kwargs)}/{identifier}/cancel"
        return self._create(path_=path, **kwargs)

    def _simulate_credit(self, identifier, **kwargs):
        """Simulate the credit of a crossborder transfer (test mode only)."""
        path = f"{self._build_path(**kwargs)}/{identifier}/simulate_credit"
        return self._create(path_=path, **kwargs)
