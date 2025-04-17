"""Module to hold the payment_intents manager."""

from fintoc.mixins import ManagerMixin


class PaymentIntentsManager(ManagerMixin):

    """Represents a payment_intents manager."""

    resource = "payment_intent"
    methods = ["list", "get", "create"]
