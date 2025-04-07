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
        # Call the method we want to test
        links = list(self.fintoc.links.all())

        # Check that the links were returned and contain the expected data
        assert len(links) > 0
        for link in links:
            assert link.method == "get"
            assert link.url == "links"

    def test_links_get(self):
        """Test that fintoc.links.get(link_id) calls the correct URL."""
        # Set up test data
        link_token = "test_link_token"
        
        # Call the method we want to test
        link = self.fintoc.links.get(link_token)
        
        # Check that the link was returned and contains the expected data
        assert link.method == "get"
        assert link.url == f"links/{link_token}"
    
    def test_links_update(self):
        """Test that fintoc.links.update() calls the correct URL."""
        # Set up test data
        link_token = "test_link_token"
        update_data = {
            "active": False
        }
        
        # Call the method we want to test
        updated_link = self.fintoc.links.update(link_token, **update_data)
        
        # Check that the link was updated with the expected data
        assert updated_link.method == "patch"
        assert updated_link.url == f"links/{link_token}"
        assert updated_link.json.active == update_data["active"]

    def test_links_delete(self):
        """Test that fintoc.links.delete() calls the correct URL."""
        # Set up test data
        link_id = "test_link_id"
        
        # Call the method we want to test
        result = self.fintoc.links.delete(link_id)
        
        # The delete method should return the ID of the deleted resource
        assert result == link_id
        
    def test_link_accounts_all(self):
        """Test getting accounts from a link."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Now get all accounts for this link
        accounts = list(link.accounts.all())

        assert link.accounts._client.params['link_token'] == link_token 
        
        # Check that accounts were returned and contain the expected data
        assert len(accounts) > 0
        for account in accounts:
            assert account.method == "get"
            assert account.url == "accounts"

    def test_link_account_get(self):
        """Test getting a specific account from a link."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Now get a specific account for this link
        account_id = "test_account_id"
        account = link.accounts.get(account_id)
        
        # Check that the account was returned with the expected data
        assert account.method == "get"
        assert account.url == f"accounts/{account_id}"
        
        # Verify that the link_token is in the client params
        assert link.accounts._client.params['link_token'] == link_token
        assert account._client.params['link_token'] == link_token

    def test_account_movements_all(self):
        """Test getting movements from an account."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Get an account from the link
        account_id = "test_account_id"
        account = link.accounts.get(account_id)
        
        # Now get all movements for this account
        movements = list(account.movements.all())
        
        # Verify that the link_token is in the client params
        assert account.movements._client.params['link_token'] == link_token
        
        # Check that movements were returned and contain the expected data
        assert len(movements) > 0
        for movement in movements:
            assert movement.method == "get"
            assert movement.url == f"accounts/{account.id}/movements"
            assert movement._client.params['link_token'] == link_token

    def test_account_movement_get(self):
        """Test getting a specific movement from an account."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Get an account from the link
        account_id = "test_account_id"
        account = link.accounts.get(account_id)
        
        # Now get a specific movement for this account
        movement_id = "test_movement_id"
        movement = account.movements.get(movement_id)
        
        # Check that the movement was returned with the expected data
        assert movement.method == "get"
        assert movement.url == f"accounts/{account.id}/movements/{movement_id}"
        
        # Verify that the link_token is in the client params
        assert movement._client.params['link_token'] == link_token

    def test_link_subscriptions_all(self):
        """Test getting all subscriptions from a link."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Now get all subscriptions for this link
        subscriptions = list(link.subscriptions.all())
        
        # Verify that the link_token is in the client params
        assert link.subscriptions._client.params['link_token'] == link_token
        
        # Check that subscriptions were returned and contain the expected data
        assert len(subscriptions) > 0
        for subscription in subscriptions:
            assert subscription.method == "get"
            assert subscription.url == "subscriptions"
            assert subscription._client.params['link_token'] == link_token

    def test_link_subscription_get(self):
        """Test getting a specific subscription from a link."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Now get a specific subscription for this link
        subscription_id = "test_subscription_id"
        subscription = link.subscriptions.get(subscription_id)
        
        # Check that the subscription was returned with the expected data
        assert subscription.method == "get"
        assert subscription.url == f"subscriptions/{subscription_id}"
        
        # Verify that the link_token is in the client params
        assert subscription._client.params['link_token'] == link_token

    def test_link_tax_returns_all(self):
        """Test getting all tax returns from a link."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Now get all tax returns for this link
        tax_returns = list(link.tax_returns.all())
        
        # Verify that the link_token is in the client params
        assert link.tax_returns._client.params['link_token'] == link_token
        
        # Check that tax returns were returned and contain the expected data
        assert len(tax_returns) > 0
        for tax_return in tax_returns:
            assert tax_return.method == "get"
            assert tax_return.url == "tax_returns"
            assert tax_return._client.params['link_token'] == link_token

    def test_link_tax_return_get(self):
        """Test getting a specific tax return from a link."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Now get a specific tax return for this link
        tax_return_id = "test_tax_return_id"
        tax_return = link.tax_returns.get(tax_return_id)
        
        # Check that the tax return was returned with the expected data
        assert tax_return.method == "get"
        assert tax_return.url == f"tax_returns/{tax_return_id}"
        
        # Verify that the link_token is in the client params
        assert tax_return._client.params['link_token'] == link_token

    def test_link_invoices_all(self):
        """Test getting all invoices from a link."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Now get all invoices for this link
        invoices = list(link.invoices.all())
        
        # Verify that the link_token is in the client params
        assert link.invoices._client.params['link_token'] == link_token
        
        # Check that invoices were returned and contain the expected data
        assert len(invoices) > 0
        for invoice in invoices:
            assert invoice.method == "get"
            assert invoice.url == "invoices"
            assert invoice._client.params['link_token'] == link_token

    def test_link_invoice_get(self):
        """Test getting a specific invoice from a link."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Now get a specific invoice for this link
        invoice_id = "test_invoice_id"
        invoice = link.invoices.get(invoice_id)
        
        # Check that the invoice was returned with the expected data
        assert invoice.method == "get"
        assert invoice.url == f"invoices/{invoice_id}"
        
        # Verify that the link_token is in the client params
        assert invoice._client.params['link_token'] == link_token

    def test_link_refresh_intents_all(self):
        """Test getting all refresh intents from a link."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Now get all refresh intents for this link
        refresh_intents = list(link.refresh_intents.all())
        
        # Verify that the link_token is in the client params
        assert link.refresh_intents._client.params['link_token'] == link_token
        
        # Check that refresh intents were returned and contain the expected data
        assert len(refresh_intents) > 0
        for refresh_intent in refresh_intents:
            assert refresh_intent.method == "get"
            assert refresh_intent.url == "refresh_intents"
            assert refresh_intent._client.params['link_token'] == link_token

    def test_link_refresh_intent_get(self):
        """Test getting a specific refresh intent from a link."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Now get a specific refresh intent for this link
        refresh_intent_id = "test_refresh_intent_id"
        refresh_intent = link.refresh_intents.get(refresh_intent_id)
        
        # Check that the refresh intent was returned with the expected data
        assert refresh_intent.method == "get"
        assert refresh_intent.url == f"refresh_intents/{refresh_intent_id}"
        
        # Verify that the link_token is in the client params
        assert refresh_intent._client.params['link_token'] == link_token

    def test_link_refresh_intent_create(self):
        """Test creating a refresh intent for a link."""
        # First get a link
        link_token = "test_link_token"
        link = self.fintoc.links.get(link_token)
        
        # Create a refresh intent for this link
        refresh_intent = link.refresh_intents.create(
            refresh_type="only_last"
        )
        
        # Check that the refresh intent was created with the expected data
        assert refresh_intent.method == "post"
        assert refresh_intent.url == "refresh_intents"
        assert refresh_intent.json.refresh_type == "only_last"
        
        # Verify that the link_token is in the client params
        assert refresh_intent._client.params['link_token'] == link_token

    def test_charges_all(self):
        """Test getting all charges."""
        # Call the method we want to test
        charges = list(self.fintoc.charges.all())
        
        # Check that charges were returned and contain the expected data
        assert len(charges) > 0
        for charge in charges:
            assert charge.method == "get"
            assert charge.url == "charges"

    def test_charge_get(self):
        """Test getting a specific charge."""
        # Set up test data
        charge_id = "test_charge_id"
        
        # Call the method we want to test
        charge = self.fintoc.charges.get(charge_id)
        
        # Check that the charge was returned with the expected data
        assert charge.method == "get"
        assert charge.url == f"charges/{charge_id}"

    def test_charge_create(self):
        """Test creating a charge."""
        # Set up test data
        charge_data = {
            "amount": 1000,
            "currency": "CLP",
            "payment_method": "bank_transfer"
        }
        
        # Call the method we want to test
        charge = self.fintoc.charges.create(**charge_data)
        
        # Check that the charge was created with the expected data
        assert charge.method == "post"
        assert charge.url == "charges"
        assert charge.json.amount == charge_data["amount"]
        assert charge.json.currency == charge_data["currency"]
        assert charge.json.payment_method == charge_data["payment_method"]

    def test_payment_intents_all(self):
        """Test getting all payment intents."""
        # Call the method we want to test
        payment_intents = list(self.fintoc.payment_intents.all())
        
        # Check that payment intents were returned and contain the expected data
        assert len(payment_intents) > 0
        for payment_intent in payment_intents:
            assert payment_intent.method == "get"
            assert payment_intent.url == "payment_intents"

    def test_payment_intent_get(self):
        """Test getting a specific payment intent."""
        # Set up test data
        payment_intent_id = "test_payment_intent_id"
        
        # Call the method we want to test
        payment_intent = self.fintoc.payment_intents.get(payment_intent_id)
        
        # Check that the payment intent was returned with the expected data
        assert payment_intent.method == "get"
        assert payment_intent.url == f"payment_intents/{payment_intent_id}"

    def test_payment_intent_create(self):
        """Test creating a payment intent."""
        # Set up test data
        payment_intent_data = {
            "amount": 1000,
            "currency": "CLP",
            "payment_method": "bank_transfer"
        }
        
        # Call the method we want to test
        payment_intent = self.fintoc.payment_intents.create(**payment_intent_data)
        
        # Check that the payment intent was created with the expected data
        assert payment_intent.method == "post"
        assert payment_intent.url == "payment_intents"
        assert payment_intent.json.amount == payment_intent_data["amount"]
        assert payment_intent.json.currency == payment_intent_data["currency"]
        assert payment_intent.json.payment_method == payment_intent_data["payment_method"]

    def test_subscription_intents_all(self):
        """Test getting all subscription intents."""
        # Call the method we want to test
        subscription_intents = list(self.fintoc.subscription_intents.all())
        
        # Check that subscription intents were returned and contain the expected data
        assert len(subscription_intents) > 0
        for subscription_intent in subscription_intents:
            assert subscription_intent.method == "get"
            assert subscription_intent.url == "subscription_intents"

    def test_subscription_intent_get(self):
        """Test getting a specific subscription intent."""
        # Set up test data
        subscription_intent_id = "test_subscription_intent_id"
        
        # Call the method we want to test
        subscription_intent = self.fintoc.subscription_intents.get(subscription_intent_id)
        
        # Check that the subscription intent was returned with the expected data
        assert subscription_intent.method == "get"
        assert subscription_intent.url == f"subscription_intents/{subscription_intent_id}"

    def test_subscription_intent_create(self):
        """Test creating a subscription intent."""
        # Set up test data
        subscription_intent_data = {
            "amount": 1000,
            "currency": "CLP"
        }
        
        # Call the method we want to test
        subscription_intent = self.fintoc.subscription_intents.create(**subscription_intent_data)
        
        # Check that the subscription intent was created with the expected data
        assert subscription_intent.method == "post"
        assert subscription_intent.url == "subscription_intents"
        assert subscription_intent.json.amount == subscription_intent_data["amount"]
        assert subscription_intent.json.currency == subscription_intent_data["currency"]

    def test_webhook_endpoints_all(self):
        """Test getting all webhook endpoints."""
        # Call the method we want to test
        webhook_endpoints = list(self.fintoc.webhook_endpoints.all())
        
        # Check that webhook endpoints were returned and contain the expected data
        assert len(webhook_endpoints) > 0
        for webhook_endpoint in webhook_endpoints:
            assert webhook_endpoint.method == "get"
            assert webhook_endpoint.url == "webhook_endpoints"

    def test_webhook_endpoint_get(self):
        """Test getting a specific webhook endpoint."""
        # Set up test data
        webhook_endpoint_id = "test_webhook_endpoint_id"
        
        # Call the method we want to test
        webhook_endpoint = self.fintoc.webhook_endpoints.get(webhook_endpoint_id)
        
        # Check that the webhook endpoint was returned with the expected data
        assert webhook_endpoint.method == "get"
        assert webhook_endpoint.url == f"webhook_endpoints/{webhook_endpoint_id}"

    def test_webhook_endpoint_create(self):
        """Test creating a webhook endpoint."""
        # Set up test data
        webhook_endpoint_data = {
            "url": "https://example.com/webhook",
            "enabled_events": ["movement.created", "link.updated"]
        }
        
        # Call the method we want to test
        webhook_endpoint = self.fintoc.webhook_endpoints.create(**webhook_endpoint_data)
        
        # Check that the webhook endpoint was created with the expected data
        assert webhook_endpoint.method == "post"
        assert webhook_endpoint.url == "webhook_endpoints"
        assert webhook_endpoint.json.url == webhook_endpoint_data["url"]
        assert webhook_endpoint.json.enabled_events == webhook_endpoint_data["enabled_events"]

    def test_webhook_endpoint_update(self):
        """Test updating a webhook endpoint."""
        # Set up test data
        webhook_endpoint_id = "test_webhook_endpoint_id"
        update_data = {
            "enabled_events": ["refund.succeeded", "link.updated", "payment_intent.failed"]
        }
        
        # Call the method we want to test
        webhook_endpoint = self.fintoc.webhook_endpoints.update(webhook_endpoint_id, **update_data)
        
        # Check that the webhook endpoint was updated with the expected data
        assert webhook_endpoint.method == "patch"
        assert webhook_endpoint.url == f"webhook_endpoints/{webhook_endpoint_id}"
        assert webhook_endpoint.json.enabled_events == update_data["enabled_events"]

    def test_webhook_endpoint_delete(self):
        """Test deleting a webhook endpoint."""
        # Set up test data
        webhook_endpoint_id = "test_webhook_endpoint_id"
        
        # Call the method we want to test
        result = self.fintoc.webhook_endpoints.delete(webhook_endpoint_id)
        
        # The delete method should return the ID of the deleted resource
        assert result == webhook_endpoint_id


if __name__ == "__main__":
    pytest.main()