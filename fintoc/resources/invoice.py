"""Module to hold the Invoice resource."""

from fintoc.mixins import ResourceMixin


class Invoice(ResourceMixin):

    """Represents a Fintoc Invoice."""

    mappings = {
        "issuer": "taxpayer",
        "receiver": "taxpayer",
    }
