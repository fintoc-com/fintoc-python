"""Module to hold the refunds manager."""

from fintoc.mixins import ManagerMixin


class RefundsManager(ManagerMixin):

    """Represents a refunds manager."""

    resource = "refund"
    methods = ["list", "get", "create", "cancel"]

    def _cancel(self, identifier, **kwargs):
        """Expire a refund."""
        path = f"{self._build_path(**kwargs)}/{identifier}/cancel"
        return self._create(path_=path, **kwargs)
