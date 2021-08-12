"""Module to hold the movements manager."""

from fintoc.mixins import ManagerMixin


class MovementsManager(ManagerMixin):

    """Represents a movements manager."""

    resource = "movement"
    methods = ["all", "get"]
