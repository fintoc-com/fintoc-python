"""Module to hold the links manager."""

from fintoc.mixins import ManagerMixin


class LinksManager(ManagerMixin):

    """Represents a links manager."""

    resource = "link"
    methods = ["list", "get", "update", "delete", "exchange"]

    def _exchange(self, exchange_token, **kwargs):
        """Exchange the widget's :exchange_token: for its link."""
        path = f"{self._build_path(**kwargs)}/exchange"
        link = self._request_resource(
            "get", path, exchange_token=exchange_token, **kwargs
        )
        return self.post_get_handler(link, link.link_token)

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
