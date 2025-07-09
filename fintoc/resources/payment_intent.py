"""Module to hold the PaymentIntent resource."""

from fintoc.mixins import ResourceMixin


class PaymentIntent(ResourceMixin):

    """Represents a Fintoc Payment Intent."""

    mappings = {
        "recipient_account": "transfer_account",
        "sender_account": "transfer_account",
    }
