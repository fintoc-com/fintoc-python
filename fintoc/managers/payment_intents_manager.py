"""Module to hold the payment_intents manager."""

from fintoc.mixins import ManagerMixin


class PaymentIntentsManager(ManagerMixin):

    """Represents a payment_intents manager."""

    resource = "payment_intent"
    methods = ["list", "get", "create", "expire", "check_eligibility"]

    def _expire(self, identifier, **kwargs):
        """Expire a payment intent."""
        path = f"{self._build_path(**kwargs)}/{identifier}/expire"
        return self._create(path_=path, **kwargs)

    def _check_eligibility(self, **kwargs):
        """Check eligibility for a payment intent."""
        path = f"{self._build_path(**kwargs)}/check_eligibility"
        return self._create(path_=path, **kwargs)
