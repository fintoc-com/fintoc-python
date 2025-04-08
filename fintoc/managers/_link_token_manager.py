"""Module to hold the link token manager."""

from fintoc.mixins import ManagerMixin


class LinkTokenManager(ManagerMixin):
    """Base class for managers that require a link token."""

    def __init__(self, path, client, link_token=None):
        super().__init__(path, client)
        self._link_token = link_token

    def _all(self, **kwargs):
        return super()._all(**{**kwargs, "link_token": self._link_token})

    def _get(self, identifier, **kwargs):
        return super()._get(identifier, **{**kwargs, "link_token": self._link_token})

    def _create(self, **kwargs):
        return super()._create(**{**kwargs, "link_token": self._link_token})
