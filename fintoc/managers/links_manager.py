from fintoc.mixins import ManagerMixin


class LinksManager(ManagerMixin):
    resource = "link"
    methods = ["all", "get", "update", "delete"]

    def _post_get_handler(self, object_, id_, **kwargs):
        object_._client_data = object_._client_data.extend(params={"link_token": id_})
        object_.link_token = id_
        return object_

    def _post_update_handler(self, object_, id_, **kwargs):
        object_._client_data = object_._client_data.extend(params={"link_token": id_})
        object_.link_token = id_
        return object_
