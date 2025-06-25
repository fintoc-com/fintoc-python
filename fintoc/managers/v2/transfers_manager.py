"""Module to hold the transfers manager."""

from fintoc.mixins import ManagerMixin


class TransfersManager(ManagerMixin):
    """Represents a transfers manager."""

    resource = "transfer"
    methods = ["list", "get", "create", "return_"]

    def _return_(self, **kwargs):
        """Return a transfer."""
        path = f"{self._build_path(**kwargs)}/return"
        return self._create(path_=path, **kwargs)
