"""Module to hold the invoices manager."""

from fintoc.mixins import ManagerMixin


class InvoicesManager(ManagerMixin):
    """Represents an invoices manager."""

    resource = "invoice"
    methods = ["list", "get", "add_lines", "remove_lines"]

    def _add_lines(self, identifier, **kwargs):
        """Add line items to an invoice."""
        path = f"{self._build_path(**kwargs)}/{identifier}/add_lines"
        return self._create(path_=path, **kwargs)

    def _remove_lines(self, identifier, **kwargs):
        """Remove line items from an invoice."""
        path = f"{self._build_path(**kwargs)}/{identifier}/remove_lines"
        return self._create(path_=path, **kwargs)
