"""Module to hold the charges manager."""

from fintoc.mixins import ManagerMixin


class ChargesManager(ManagerMixin):

    """Represents a charges manager."""

    resource = "charge"
    methods = ["list", "get", "create"]
