"""Module to hold the payment_links manager."""

from fintoc.mixins import ManagerMixin


class PaymentLinksManager(ManagerMixin):

    """Represents a payment_links manager."""

    resource = "payment_link"
    methods = ["list", "get", "create", "cancel"]

    def _cancel(self, identifier, **kwargs):
        """Cancel a payment link."""
        path = f"{self._build_path(**kwargs)}/{identifier}/cancel"
        return self._update(identifier, path_=path, **kwargs)
