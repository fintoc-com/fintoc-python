"""Module to hold the accounts manager."""

from fintoc.mixins import ManagerMixin


class AccountsManager(ManagerMixin):

    """Represents an accounts manager."""

    resource = "account"
    methods = ["all", "get"]

    def __init__(self, path, client, link_token=None):
        super().__init__(path, client)
        self._link_token = link_token

    def post_get_handler(self, object_, identifier, **kwargs):
        # pylint: disable=protected-access
        object_._link_token = self._link_token
        return object_

    def post_all_handler(self, objects, **kwargs):
        # pylint: disable=protected-access
        if isinstance(objects, list):
            for obj in objects:
                obj._link_token = self._link_token
            return objects
        else:
            def modified_generator():
                for obj in objects:
                    obj._link_token = self._link_token
                    yield obj

            return modified_generator()

    def _all(self, **kwargs):
        return super()._all(**{**kwargs, "link_token": self._link_token})

    def _get(self, identifier, **kwargs):
        return super()._get(identifier, **{**kwargs, "link_token": self._link_token})
