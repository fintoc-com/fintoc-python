"""
Core module to house the Fintoc object of the Fintoc Python SDK.
"""

from fintoc.client import Client
from fintoc.constants import API_BASE_URL
from fintoc.managers import (
    AccountsManager,
    ChargesManager,
    CheckoutSessionsManager,
    InvoicesManager,
    LinksManager,
    PaymentIntentsManager,
    RefreshIntentsManager,
    SubscriptionIntentsManager,
    SubscriptionsManager,
    TaxReturnsManager,
    WebhookEndpointsManager,
)
from fintoc.managers.v2 import AccountNumbersManager
from fintoc.managers.v2 import AccountsManager as AccountsManagerV2
from fintoc.managers.v2 import (
    AccountVerificationsManager,
    EntitiesManager,
    SimulateManager,
    TransfersManager,
)
from fintoc.version import __version__


# pylint: disable=too-many-instance-attributes
class Fintoc:

    """Encapsulates the core object's behaviour and methods."""

    def __init__(self, api_key, api_version=None, jws_private_key=None):
        self._client = Client(
            base_url=f"{API_BASE_URL}",
            api_key=api_key,
            api_version=api_version,
            user_agent=f"fintoc-python/{__version__}",
            jws_private_key=jws_private_key,
        )
        self.charges = ChargesManager("/v1/charges", self._client)
        self.checkout_sessions = CheckoutSessionsManager(
            "/v1/checkout_sessions", self._client
        )
        self.links = LinksManager("/v1/links", self._client)
        self.payment_intents = PaymentIntentsManager(
            "/v1/payment_intents", self._client
        )
        self.subscriptions = SubscriptionsManager("/v1/subscriptions", self._client)
        self.subscription_intents = SubscriptionIntentsManager(
            "/v1/subscription_intents", self._client
        )
        self.webhook_endpoints = WebhookEndpointsManager(
            "/v1/webhook_endpoints", self._client
        )
        self.accounts = AccountsManager("/v1/accounts", self._client)
        self.refresh_intents = RefreshIntentsManager(
            "/v1/refresh_intents", self._client
        )
        self.tax_returns = TaxReturnsManager("/v1/tax_returns", self._client)
        self.invoices = InvoicesManager("/v1/invoices", self._client)

        self.v2 = _FintocV2(self._client)


class _FintocV2:
    def __init__(self, client):
        self.transfers = TransfersManager("/v2/transfers", client)
        self.accounts = AccountsManagerV2("/v2/accounts", client)
        self.account_numbers = AccountNumbersManager("/v2/account_numbers", client)
        self.account_verifications = AccountVerificationsManager(
            "/v2/account_verifications", client
        )
        self.entities = EntitiesManager("/v2/entities", client)
        self.simulate = SimulateManager("/v2/simulate", client)
