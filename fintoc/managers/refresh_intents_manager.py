"""Module to hold the refresh_intents manager."""

from fintoc.mixins import ManagerMixin


class RefreshIntentsManager(ManagerMixin):

    """Represents a refresh_intents manager."""

    resource = "refresh_intent"
    methods = ["all", "get", "create"]

    def __init__(self, path, client, link_token=None):
        super().__init__(path, client)
        self._link_token = link_token

    def _all(self, **kwargs):
        return super()._all(**{**kwargs, "link_token": self._link_token})

    def _get(self, identifier, **kwargs):
        return super()._get(identifier, **{**kwargs, "link_token": self._link_token})

    def _create(self, **kwargs):
        return super()._create(**{**kwargs, "link_token": self._link_token})
