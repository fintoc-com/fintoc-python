from fintoc.mixins import ManagerMixin


class LinksManager(ManagerMixin):
    resource = "link"
    methods = ["all", "get", "update", "delete"]

    def post_get_handler(self, object_, identifier, **kwargs):
        object_._client = self._client.extend(params={"link_token": identifier})
        object_.link_token = identifier
        return object_

    def post_update_handler(self, object_, identifier, **kwargs):
        object_._client = self._client.extend(params={"link_token": identifier})
        object_.link_token = identifier
        return object_
