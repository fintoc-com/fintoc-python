"""Module to hold the crossborder beneficiaries manager."""

from fintoc.mixins import ManagerMixin


class CrossborderBeneficiariesManager(ManagerMixin):
    """Represents a crossborder beneficiaries manager."""

    resource = "crossborder_beneficiary"
    methods = ["list", "get", "create", "delete"]
