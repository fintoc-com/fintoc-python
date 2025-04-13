"""Module to hold the simulate manager."""

from fintoc.mixins import ManagerMixin


class SimulateManager(ManagerMixin):
    """Represents a simulate manager for testing purposes."""

    resource = "transfer"
    methods = ["receive_transfer"]

    def _receive_transfer(self, **kwargs):
        path = f"{self._build_path(**kwargs)}/receive_transfer"
        return self._create(path_=path, **kwargs)
