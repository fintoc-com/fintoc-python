from fintoc.mixins import ManagerMixin


class LinksManager(ManagerMixin):
    resource = "link"
    methods = ["all", "get"]
