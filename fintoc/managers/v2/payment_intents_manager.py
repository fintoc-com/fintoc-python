# pylint: disable=duplicate-code
"""Module to hold the payment_intents manager."""

from fintoc.mixins import ManagerMixin


class PaymentIntentsManager(ManagerMixin):
    """Represents a payment_intents manager."""

    resource = "payment_intent"
    methods = ["list", "get", "create", "check_eligibility", "cancel", "voucher_url"]

    def _check_eligibility(self, idempotency_key=None, **kwargs):
        """Check whether a payment passes the transfer limits."""
        path = f"{self._build_path(**kwargs)}/check_eligibility"
        return self._request_resource(
            "post",
            path,
            resource="payment_eligibility",
            idempotency_key=idempotency_key,
            **kwargs,
        )

    def _cancel(self, identifier, **kwargs):
        """Cancel a payment intent."""
        path = f"{self._build_path(**kwargs)}/{identifier}/cancel"
        return self._create(path_=path, **kwargs)

    def _voucher_url(self, identifier, **kwargs):
        """Get a URL to download the transfer voucher of a payment intent."""
        path = f"{self._build_path(**kwargs)}/{identifier}/voucher_url"
        return self._request_resource("get", path, resource="voucher_url", **kwargs)
