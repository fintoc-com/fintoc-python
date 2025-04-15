"""
Core module to house the Fintoc object of the Fintoc Python SDK.
"""

from fintoc.client import Client
from fintoc.constants import API_BASE_URL, API_VERSION
from fintoc.managers import (
    AccountsManager,
    ChargesManager,
    InvoicesManager,
    LinksManager,
    PaymentIntentsManager,
    RefreshIntentsManager,
    SubscriptionIntentsManager,
    SubscriptionsManager,
    TaxReturnsManager,
    WebhookEndpointsManager,
)
from fintoc.version import __version__


# pylint: disable=too-many-instance-attributes
class Fintoc:

    """Encapsulates the core object's behaviour and methods."""

    def __init__(self, api_key, api_version=None):
        self._client = Client(
            base_url=f"{API_BASE_URL}/{API_VERSION}",
            api_key=api_key,
            api_version=api_version,
            user_agent=f"fintoc-python/{__version__}",
        )
        self.charges = ChargesManager("/charges", self._client)
        self.links = LinksManager("/links", self._client)
        self.payment_intents = PaymentIntentsManager("/payment_intents", self._client)
        self.subscriptions = SubscriptionsManager("/subscriptions", self._client)
        self.subscription_intents = SubscriptionIntentsManager(
            "/subscription_intents", self._client
        )
        self.webhook_endpoints = WebhookEndpointsManager(
            "/webhook_endpoints", self._client
        )
        self.accounts = AccountsManager("/accounts", self._client)
        self.refresh_intents = RefreshIntentsManager("/refresh_intents", self._client)
        self.tax_returns = TaxReturnsManager("/tax_returns", self._client)
        self.invoices = InvoicesManager("/invoices", self._client)
