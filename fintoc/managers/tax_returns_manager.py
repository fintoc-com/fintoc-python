"""Module to hold the tax_returns manager."""

from fintoc.mixins import ManagerMixin


class TaxReturnsManager(ManagerMixin):

    """Represents a tax_returns manager."""

    resource = "tax_return"
    methods = ["all", "get"]

    def __init__(self, path, client, link_token=None):
        super().__init__(path, client)
        self._link_token = link_token

    def _all(self, **kwargs):
        return super()._all(**{**kwargs, "link_token": self._link_token})

    def _get(self, identifier, **kwargs):
        return super()._get(identifier, **{**kwargs, "link_token": self._link_token})
