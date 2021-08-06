from fintoc.mixins import ManagerMixin


class InvoicesManager(ManagerMixin):
    resource = "invoice"
    methods = ["all"]
