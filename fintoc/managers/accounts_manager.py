from fintoc.mixins import ManagerMixin


class AccountsManager(ManagerMixin):
    resource = "account"
    methods = ["all", "get"]
