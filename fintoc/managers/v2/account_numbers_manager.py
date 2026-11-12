"""Module to hold the account numbers manager."""

from fintoc.mixins import ManagerMixin


class AccountNumbersManager(ManagerMixin):
    """Represents an account numbers manager."""

    resource = "account_number"
    methods = ["list", "get", "update", "create", "delete", "certificate"]

    def _certificate(self, identifier, **kwargs):
        """Get a signed link to download the PDF certificate of an account number."""
        path = f"{self._build_path(**kwargs)}/{identifier}/certificate"
        return self._request_resource(
            "get", path, resource="account_certificate", **kwargs
        )
