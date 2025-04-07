"""Integration tests for the Fintoc core object."""

import pytest

from fintoc.core import Fintoc


class TestFintocIntegration:
    """Test class to verify Fintoc core object integration with managers."""

    @pytest.fixture(autouse=True)
    def patch_http_client(self, patch_http_client):
        """Use the mock HTTP client from conftest.py."""
        pass

    def setup_method(self):
        """Set up the test environment."""
        self.api_key = "test_api_key"
        self.fintoc = Fintoc(self.api_key)

    def test_links_all(self):
        """Test that fintoc.links.all() calls the correct URL."""
        links = list(self.fintoc.links.all())

        assert len(links) > 0
        for link in links:
            assert link.method == "get"
            assert link.url == "links"

    def test_links_get(self):
        """Test that fintoc.links.get(link_id) calls the correct URL."""
        link_token = "test_link_token"

        link = self.fintoc.links.get(link_token)

        assert link.method == "get"
        assert link.url == f"links/{link_token}"

    def test_links_update(self):
        """Test that fintoc.links.update() calls the correct URL."""
        link_token = "test_link_token"
        update_data = {"active": False}

        updated_link = self.fintoc.links.update(link_token, **update_data)

        assert updated_link.method == "patch"
        assert updated_link.url == f"links/{link_token}"
        assert updated_link.json.active == update_data["active"]

    def test_links_delete(self):
        """Test that fintoc.links.delete() calls the correct URL."""
        link_id = "test_link_id"

        result = self.fintoc.links.delete(link_id)

        assert result == link_id

    def test_link_accounts_all(self):
        """Test getting accounts from a link."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        accounts = list(link.accounts.all())

        assert len(accounts) > 0
        for account in accounts:
            assert account.method == "get"
            assert account.url == "accounts"
            assert account.params.link_token == link_token

    def test_link_account_get(self):
        """Test getting a specific account from a link."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        account_id = "test_account_id"
        account = link.accounts.get(account_id)

        assert account.method == "get"
        assert account.params.link_token == link_token
        assert account.url == f"accounts/{account_id}"

    def test_account_movements_all(self):
        """Test getting movements from an account."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        account_id = "test_account_id"
        account = link.accounts.get(account_id)

        movements = list(account.movements.all())

        assert len(movements) > 0
        for movement in movements:
            assert movement.method == "get"
            assert movement.url == f"accounts/{account.id}/movements"
            assert movement.params.link_token == link_token

    def test_account_movement_get(self):
        """Test getting a specific movement from an account."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        account_id = "test_account_id"
        account = link.accounts.get(account_id)

        movement_id = "test_movement_id"
        movement = account.movements.get(movement_id)

        assert movement.method == "get"
        assert movement.url == f"accounts/{account.id}/movements/{movement_id}"
        assert movement.params.link_token == link_token

    def test_link_subscriptions_all(self):
        """Test getting all subscriptions from a link."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        subscriptions = list(link.subscriptions.all())

        assert len(subscriptions) > 0
        for subscription in subscriptions:
            assert subscription.method == "get"
            assert subscription.url == "subscriptions"

    def test_link_subscription_get(self):
        """Test getting a specific subscription from a link."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        subscription_id = "test_subscription_id"
        subscription = link.subscriptions.get(subscription_id)

        assert subscription.method == "get"
        assert subscription.url == f"subscriptions/{subscription_id}"

    def test_link_tax_returns_all(self):
        """Test getting all tax returns from a link."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        tax_returns = list(link.tax_returns.all())

        assert len(tax_returns) > 0
        for tax_return in tax_returns:
            assert tax_return.method == "get"
            assert tax_return.url == "tax_returns"
            assert tax_return.params.link_token == link_token

    def test_link_tax_return_get(self):
        """Test getting a specific tax return from a link."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        tax_return_id = "test_tax_return_id"
        tax_return = link.tax_returns.get(tax_return_id)

        assert tax_return.method == "get"
        assert tax_return.url == f"tax_returns/{tax_return_id}"

        assert tax_return.params.link_token == link_token

    def test_link_invoices_all(self):
        """Test getting all invoices from a link."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        invoices = list(link.invoices.all())

        assert len(invoices) > 0
        for invoice in invoices:
            assert invoice.method == "get"
            assert invoice.url == "invoices"
            assert invoice.params.link_token == link_token

    def test_link_invoice_get(self):
        """Test getting a specific invoice from a link."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        invoice_id = "test_invoice_id"
        invoice = link.invoices.get(invoice_id)

        assert invoice.method == "get"
        assert invoice.url == f"invoices/{invoice_id}"
        assert invoice.params.link_token == link_token

    def test_link_refresh_intents_all(self):
        """Test getting all refresh intents from a link."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        refresh_intents = list(link.refresh_intents.all())

        assert len(refresh_intents) > 0
        for refresh_intent in refresh_intents:
            assert refresh_intent.method == "get"
            assert refresh_intent.url == "refresh_intents"
            assert refresh_intent.params.link_token == link_token

    def test_link_refresh_intent_get(self):
        """Test getting a specific refresh intent from a link."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        refresh_intent_id = "test_refresh_intent_id"
        refresh_intent = link.refresh_intents.get(refresh_intent_id)

        assert refresh_intent.method == "get"
        assert refresh_intent.url == f"refresh_intents/{refresh_intent_id}"

        assert refresh_intent.params.link_token == link_token

    def test_link_refresh_intent_create(self):
        """Test creating a refresh intent for a link."""
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)

        refresh_intent = link.refresh_intents.create(refresh_type="only_last")

        assert refresh_intent.method == "post"
        assert refresh_intent.url == "refresh_intents"
        assert refresh_intent.json.refresh_type == "only_last"
        assert refresh_intent.json.link_token == link_token

    def test_charges_all(self):
        """Test getting all charges."""
        charges = list(self.fintoc.charges.all())

        assert len(charges) > 0
        for charge in charges:
            assert charge.method == "get"
            assert charge.url == "charges"

    def test_charge_get(self):
        """Test getting a specific charge."""
        charge_id = "test_charge_id"

        charge = self.fintoc.charges.get(charge_id)

        assert charge.method == "get"
        assert charge.url == f"charges/{charge_id}"

    def test_charge_create(self):
        """Test creating a charge."""
        charge_data = {
            "amount": 1000,
            "currency": "CLP",
            "payment_method": "bank_transfer",
        }

        charge = self.fintoc.charges.create(**charge_data)

        assert charge.method == "post"
        assert charge.url == "charges"
        assert charge.json.amount == charge_data["amount"]
        assert charge.json.currency == charge_data["currency"]
        assert charge.json.payment_method == charge_data["payment_method"]

    def test_payment_intents_all(self):
        """Test getting all payment intents."""
        payment_intents = list(self.fintoc.payment_intents.all())

        assert len(payment_intents) > 0
        for payment_intent in payment_intents:
            assert payment_intent.method == "get"
            assert payment_intent.url == "payment_intents"

    def test_payment_intent_get(self):
        """Test getting a specific payment intent."""
        payment_intent_id = "test_payment_intent_id"

        payment_intent = self.fintoc.payment_intents.get(payment_intent_id)

        assert payment_intent.method == "get"
        assert payment_intent.url == f"payment_intents/{payment_intent_id}"

    def test_payment_intent_create(self):
        """Test creating a payment intent."""
        payment_intent_data = {
            "amount": 1000,
            "currency": "CLP",
            "payment_method": "bank_transfer",
        }

        payment_intent = self.fintoc.payment_intents.create(**payment_intent_data)

        assert payment_intent.method == "post"
        assert payment_intent.url == "payment_intents"
        assert payment_intent.json.amount == payment_intent_data["amount"]
        assert payment_intent.json.currency == payment_intent_data["currency"]
        assert (
            payment_intent.json.payment_method == payment_intent_data["payment_method"]
        )

    def test_subscription_intents_all(self):
        """Test getting all subscription intents."""
        subscription_intents = list(self.fintoc.subscription_intents.all())

        assert len(subscription_intents) > 0
        for subscription_intent in subscription_intents:
            assert subscription_intent.method == "get"
            assert subscription_intent.url == "subscription_intents"

    def test_subscription_intent_get(self):
        """Test getting a specific subscription intent."""
        subscription_intent_id = "test_subscription_intent_id"

        subscription_intent = self.fintoc.subscription_intents.get(
            subscription_intent_id
        )

        assert subscription_intent.method == "get"
        assert (
            subscription_intent.url == f"subscription_intents/{subscription_intent_id}"
        )

    def test_subscription_intent_create(self):
        """Test creating a subscription intent."""
        subscription_intent_data = {"amount": 1000, "currency": "CLP"}

        subscription_intent = self.fintoc.subscription_intents.create(
            **subscription_intent_data
        )

        assert subscription_intent.method == "post"
        assert subscription_intent.url == "subscription_intents"
        assert subscription_intent.json.amount == subscription_intent_data["amount"]
        assert subscription_intent.json.currency == subscription_intent_data["currency"]

    def test_webhook_endpoints_all(self):
        """Test getting all webhook endpoints."""
        webhook_endpoints = list(self.fintoc.webhook_endpoints.all())

        assert len(webhook_endpoints) > 0
        for webhook_endpoint in webhook_endpoints:
            assert webhook_endpoint.method == "get"
            assert webhook_endpoint.url == "webhook_endpoints"

    def test_webhook_endpoint_get(self):
        """Test getting a specific webhook endpoint."""
        webhook_endpoint_id = "test_webhook_endpoint_id"

        webhook_endpoint = self.fintoc.webhook_endpoints.get(webhook_endpoint_id)

        assert webhook_endpoint.method == "get"
        assert webhook_endpoint.url == f"webhook_endpoints/{webhook_endpoint_id}"

    def test_webhook_endpoint_create(self):
        """Test creating a webhook endpoint."""
        webhook_endpoint_data = {
            "url": "https://example.com/webhook",
            "enabled_events": ["movement.created", "link.updated"],
        }

        webhook_endpoint = self.fintoc.webhook_endpoints.create(**webhook_endpoint_data)

        assert webhook_endpoint.method == "post"
        assert webhook_endpoint.url == "webhook_endpoints"
        assert webhook_endpoint.json.url == webhook_endpoint_data["url"]
        assert (
            webhook_endpoint.json.enabled_events
            == webhook_endpoint_data["enabled_events"]
        )

    def test_webhook_endpoint_update(self):
        """Test updating a webhook endpoint."""
        webhook_endpoint_id = "test_webhook_endpoint_id"
        update_data = {
            "enabled_events": [
                "refund.succeeded",
                "link.updated",
                "payment_intent.failed",
            ]
        }

        webhook_endpoint = self.fintoc.webhook_endpoints.update(
            webhook_endpoint_id, **update_data
        )

        assert webhook_endpoint.method == "patch"
        assert webhook_endpoint.url == f"webhook_endpoints/{webhook_endpoint_id}"
        assert webhook_endpoint.json.enabled_events == update_data["enabled_events"]

    def test_webhook_endpoint_delete(self):
        """Test deleting a webhook endpoint."""
        webhook_endpoint_id = "test_webhook_endpoint_id"

        result = self.fintoc.webhook_endpoints.delete(webhook_endpoint_id)

        assert result == webhook_endpoint_id


if __name__ == "__main__":
    pytest.main()
