"""Module to hold the organizations manager."""

from fintoc.mixins import ManagerMixin


class OrganizationsManager(ManagerMixin):

    """Represents an organizations manager."""

    resource = "organization"
    methods = ["create", "update"]
