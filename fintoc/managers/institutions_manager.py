"""Module to hold the institutions manager."""

from fintoc.mixins import ManagerMixin


class InstitutionsManager(ManagerMixin):

    """Represents an institutions manager."""

    resource = "institution"
    methods = ["list"]
