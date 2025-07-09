"""Module to hold the payment_intents manager."""

from fintoc.mixins import ManagerMixin


class PaymentIntentsManager(ManagerMixin):

    """Represents a payment_intents manager."""

    resource = "payment_intent"
    methods = ["list", "get", "create", "expire"]

    def _expire(self, identifier, **kwargs):
        """Expire a payment intent."""
        path = f"{self._build_path(**kwargs)}/{identifier}/expire"
        return self._create(path_=path, **kwargs)
