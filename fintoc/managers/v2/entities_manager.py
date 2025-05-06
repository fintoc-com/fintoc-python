"""Module to hold the entities manager."""

from fintoc.mixins import ManagerMixin


class EntitiesManager(ManagerMixin):
    """Represents an entities manager."""

    resource = "entity"
    methods = ["list", "get"]
