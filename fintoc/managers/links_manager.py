"""Module to hold the links manager."""

from fintoc.mixins import ManagerMixin


class LinksManager(ManagerMixin):

    """Represents a links manager."""

    resource = "link"
    methods = ["all", "get", "update", "delete"]

    def post_get_handler(self, object_, identifier, **kwargs):
        # pylint: disable=protected-access
        object_._client = self._client.extend(params={"link_token": identifier})
        object_._link_token = identifier
        return object_

    def post_update_handler(self, object_, identifier, **kwargs):
        # pylint: disable=protected-access
        object_._client = self._client.extend(params={"link_token": identifier})
        object_._link_token = identifier
        return object_
