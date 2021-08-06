from fintoc.mixins import ManagerMixin


class TaxRetunsManager(ManagerMixin):
    resource = "tax_return"
    methods = ["all", "get"]
