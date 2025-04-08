"""Module to hold the accounts manager."""

from fintoc.managers._link_token_manager import LinkTokenManager


class AccountsManager(LinkTokenManager):

    """Represents an accounts manager."""

    resource = "account"
    methods = ["all", "get"]

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
