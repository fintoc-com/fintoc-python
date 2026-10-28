"""Module to hold the charges manager."""

from fintoc.mixins import ManagerMixin


class ChargesManager(ManagerMixin):

    """Represents a charges manager."""

    resource = "charge"
    methods = ["list", "get", "create", "update", "cancel"]

    def _cancel(self, identifier, **kwargs):
        """Cancel a charge."""
        path = f"{self._build_path(**kwargs)}/{identifier}/cancel"
        charge = self._create(path_=path, **kwargs)
        # pylint: disable=protected-access
        charge._path = self._build_path(**kwargs)
        return charge
