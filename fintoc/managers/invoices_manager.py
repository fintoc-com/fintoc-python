"""Module to hold the invoices manager."""

from fintoc.mixins import ManagerMixin


class InvoicesManager(ManagerMixin):

    """Represents an invoices manager."""

    resource = "invoice"
    methods = ["all"]

    def __init__(self, path, client, link_token=None):
        super().__init__(path, client)
        self._link_token = link_token

    def _all(self, **kwargs):
        return super()._all(**{**kwargs, "link_token": self._link_token})
