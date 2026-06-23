"""Module to hold the invoices manager."""

from fintoc.managers.v2.lines_manager import LinesManager
from fintoc.mixins import ManagerMixin


class InvoicesManager(ManagerMixin):
    """Represents an invoices manager."""

    resource = "invoice"
    methods = ["list", "get", "add_lines", "remove_lines"]

    def __init__(self, path, client):
        super().__init__(path, client)
        self.__lines_manager = None

    @property
    def lines(self):
        """Proxies the invoice lines manager."""
        if self.__lines_manager is None:
            self.__lines_manager = LinesManager(
                "/v2/invoices/{invoice_id}/lines",
                self._client,
            )
        return self.__lines_manager

    @lines.setter
    def lines(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")

    def _add_lines(self, identifier, **kwargs):
        """Add line items to an invoice."""
        path = f"{self._build_path(**kwargs)}/{identifier}/add_lines"
        return self._create(path_=path, **kwargs)

    def _remove_lines(self, identifier, **kwargs):
        """Remove line items from an invoice."""
        path = f"{self._build_path(**kwargs)}/{identifier}/remove_lines"
        return self._create(path_=path, **kwargs)
