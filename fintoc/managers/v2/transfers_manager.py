"""Module to hold the transfers manager."""

from fintoc.mixins import ManagerMixin


class TransfersManager(ManagerMixin):
    """Represents a transfers manager."""

    resource = "transfer"
    methods = ["list", "get", "create", "return_", "receipt"]

    def _return_(self, **kwargs):
        """Return a transfer."""
        path = f"{self._build_path(**kwargs)}/return"
        return self._create(path_=path, **kwargs)

    def _receipt(self, identifier, **kwargs):
        """Get a signed link to download the PDF receipt of a transfer."""
        path = f"{self._build_path(**kwargs)}/{identifier}/receipt"
        return self._request_resource(
            "get", path, resource="transfer_receipt", **kwargs
        )
