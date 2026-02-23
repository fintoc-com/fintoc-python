"""Module to hold the payment methods manager."""

from fintoc.mixins import ManagerMixin


class PaymentMethodsManager(ManagerMixin):
    """Represents a payment methods manager."""

    resource = "payment_method"
    methods = ["list", "get"]
