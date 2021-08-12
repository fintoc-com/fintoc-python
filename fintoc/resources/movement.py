"""Module to hold the Movement resource."""

from fintoc.mixins import ResourceMixin


class Movement(ResourceMixin):

    """Represents a Fintoc Movement."""

    mappings = {
        "recipient_account": "transfer_account",
        "sender_account": "transfer_account",
    }
