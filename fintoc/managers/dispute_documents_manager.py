"""Module to hold the dispute documents manager."""

from fintoc.mixins import ManagerMixin


class DisputeDocumentsManager(ManagerMixin):
    """Represents a dispute documents manager."""

    resource = "dispute_document"
    methods = ["create"]
