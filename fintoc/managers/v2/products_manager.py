"""Module to hold the products manager."""

from fintoc.mixins import ManagerMixin


class ProductsManager(ManagerMixin):
    """Represents a products manager."""

    resource = "product"
    methods = ["create", "get", "list"]
