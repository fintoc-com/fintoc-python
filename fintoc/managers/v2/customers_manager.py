"""Module to hold the customers manager."""

from fintoc.mixins import ManagerMixin


class CustomersManager(ManagerMixin):
    """Represents a customers manager."""

    resource = "customer"
    methods = ["list", "get", "create"]
