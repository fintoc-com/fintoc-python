"""Module to hold the events manager."""

from fintoc.mixins import ManagerMixin


class EventsManager(ManagerMixin):
    """Represents an events manager."""

    resource = "event"
    methods = ["list", "get"]
