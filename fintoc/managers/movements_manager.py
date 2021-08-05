from fintoc.mixins import ManagerMixin


class MovementsManager(ManagerMixin):
    resource = "movement"
    methods = ["all", "get"]
