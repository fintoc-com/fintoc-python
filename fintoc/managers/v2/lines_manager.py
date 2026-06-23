"""Module to hold the invoice lines manager."""

from fintoc.mixins import ManagerMixin


class LinesManager(ManagerMixin):
    """Represents an invoice lines manager."""

    resource = "line"
    methods = ["update"]
