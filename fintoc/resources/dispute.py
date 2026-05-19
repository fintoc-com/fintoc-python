"""Module to hold the Dispute resource."""

from fintoc.mixins import ResourceMixin


class Dispute(ResourceMixin):
    """Represents a Fintoc Dispute."""

    mappings = {
        "documents": "dispute_document",
    }
