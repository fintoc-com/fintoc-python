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

    def test_links_list(self):
        """Test that fintoc.links.list() calls the correct URL."""
        links = list(self.fintoc.links.list())

        assert len(links) > 0
        for link in links:
            assert link.method == "get"
            assert link.url == "v1/links"

    def test_links_get(self):
        """Test that fintoc.links.get(link_id) calls the correct URL."""
        link_token = "test_link_token"

        link = self.fintoc.links.get(link_token)

        assert link.method == "get"
        assert link.url == f"v1/links/{link_token}"

    def test_links_update(self):
        """Test that fintoc.links.update() calls the correct URL."""
        link_token = "test_link_token"
        update_data = {"active": False}

        updated_link = self.fintoc.links.update(link_token, **update_data)

        assert updated_link.method == "patch"
        assert updated_link.url == f"v1/links/{link_token}"
        assert updated_link.json.active == update_data["active"]

    def test_links_delete(self):
        """Test that fintoc.links.delete() calls the correct URL."""
        link_id = "test_link_id"

        result = self.fintoc.links.delete(link_id)

        assert result == link_id

    def test_link_accounts_list(self):
        """Test getting accounts from a link."""

        def assert_accounts(accounts):
            assert len(accounts) > 0
            for account in accounts:
                assert account.method == "get"
                assert account.url == "v1/accounts"

        link_token = "test_link_token"

        # Test using the resource
        link = self.fintoc.links.get(link_token)
        assert_accounts(list(link.accounts.list()))

        # Test using directly the manager
        assert_accounts(list(self.fintoc.accounts.list(link_token=link_token)))

    def test_link_account_get(self):
        """Test getting a specific account from a link."""

        def assert_account(account):
            assert account.method == "get"
            assert account.params.link_token == link_token
            assert account.url == f"v1/accounts/{account_id}"

        link_token = "test_link_token"
        account_id = "test_account_id"

        # Test using the resource
        link = self.fintoc.links.get(link_token)
        account = link.accounts.get(account_id)
        assert_account(account)

        # Test using directly the manager
        account = self.fintoc.accounts.get(account_id, link_token=link_token)
        assert_account(account)

    def test_account_movements_list(self):
        """Test getting movements from an account."""

        def assert_movements(movements):
            assert len(movements) > 0
            for movement in movements:
                assert movement.method == "get"
                assert movement.url == f"v1/accounts/{account_id}/movements"

        link_token = "test_link_token"
        account_id = "test_account_id"

        # Test using the resource
        link = self.fintoc.links.get(link_token)
        account = link.accounts.get(account_id)
        assert_movements(list(account.movements.list()))

        # Test using directly the manager
        assert_movements(
            list(
                self.fintoc.accounts.movements.list(
                    account_id=account_id, link_token=link_token
                )
            )
        )

    def test_account_movement_get(self):
        """Test getting a specific movement from an account."""

        def assert_movement(movement):
            assert movement.method == "get"
            assert movement.url == f"v1/accounts/{account_id}/movements/{movement_id}"
            assert movement.params.link_token == link_token

        link_token = "test_link_token"
        account_id = "test_account_id"
        movement_id = "test_movement_id"

        # Test using the resource
        link = self.fintoc.links.get(link_token)
        account = link.accounts.get(account_id)
        movement = account.movements.get(movement_id)
        assert_movement(movement)

        # Test using directly the manager
        movement = self.fintoc.accounts.movements.get(
            movement_id, account_id=account_id, link_token=link_token
        )
        assert_movement(movement)

    def test_link_subscriptions_list(self):
        """Test getting all subscriptions from a link."""

        def assert_subscriptions(subscriptions):
            assert len(subscriptions) > 0
            for subscription in subscriptions:
                assert subscription.method == "get"
                assert subscription.url == "v1/subscriptions"

        link_token = "test_link_token"

        # Test using the resource. This actually should be removed, because
        # subscriptions do not depend on a link.
        link = self.fintoc.links.get(link_token)
        assert_subscriptions(list(link.subscriptions.list()))

        # Test using directly the manager
        assert_subscriptions(list(self.fintoc.subscriptions.list()))

    def test_link_subscription_get(self):
        """Test getting a specific subscription from a link."""

        def assert_subscription(subscription):
            assert subscription.method == "get"
            assert subscription.url == f"v1/subscriptions/{subscription_id}"

        link_token = "test_link_token"
        subscription_id = "test_subscription_id"

        # Test using the resource
        link = self.fintoc.links.get(link_token)
        subscription = link.subscriptions.get(subscription_id)
        assert_subscription(subscription)

        # Test using directly the manager
        subscription = self.fintoc.subscriptions.get(
            subscription_id, link_token=link_token
        )
        assert_subscription(subscription)

    def test_link_tax_returns_list(self):
        """Test getting all tax returns from a link."""

        def assert_tax_returns(tax_returns):
            assert len(tax_returns) > 0
            for tax_return in tax_returns:
                assert tax_return.method == "get"
                assert tax_return.url == "v1/tax_returns"

        link_token = "test_link_token"

        # Test using the resource
        link = self.fintoc.links.get(link_token)
        assert_tax_returns(list(link.tax_returns.list()))

        # Test using directly the manager
        assert_tax_returns(list(self.fintoc.tax_returns.list(link_token=link_token)))

    def test_link_tax_return_get(self):
        """Test getting a specific tax return from a link."""

        def assert_tax_return(tax_return):
            assert tax_return.method == "get"
            assert tax_return.url == f"v1/tax_returns/{tax_return_id}"
            assert tax_return.params.link_token == link_token

        link_token = "test_link_token"
        tax_return_id = "test_tax_return_id"

        # Test using the resource
        link = self.fintoc.links.get(link_token)
        tax_return = link.tax_returns.get(tax_return_id)
        assert_tax_return(tax_return)

        # Test using directly the manager
        tax_return = self.fintoc.tax_returns.get(tax_return_id, link_token=link_token)
        assert_tax_return(tax_return)

    def test_link_invoices_list(self):
        """Test getting all invoices from a link."""

        def assert_invoices(invoices):
            assert len(invoices) > 0
            for invoice in invoices:
                assert invoice.method == "get"
                assert invoice.url == "v1/invoices"

        link_token = "test_link_token"

        # Test using the resource
        link = self.fintoc.links.get(link_token)
        assert_invoices(list(link.invoices.list()))

        # Test using directly the manager
        assert_invoices(list(self.fintoc.invoices.list(link_token=link_token)))

    def test_link_refresh_intents_list(self):
        """Test getting all refresh intents from a link."""

        def assert_refresh_intents(refresh_intents):
            assert len(refresh_intents) > 0
            for refresh_intent in refresh_intents:
                assert refresh_intent.method == "get"
                assert refresh_intent.url == "v1/refresh_intents"

        link_token = "test_link_token"

        # Test using the resource
        link = self.fintoc.links.get(link_token)
        assert_refresh_intents(list(link.refresh_intents.list()))

        # Test using directly the manager
        assert_refresh_intents(
            list(self.fintoc.refresh_intents.list(link_token=link_token))
        )

    def test_link_refresh_intent_get(self):
        """Test getting a specific refresh intent from a link."""

        def assert_refresh_intent(refresh_intent):
            assert refresh_intent.method == "get"
            assert refresh_intent.url == f"v1/refresh_intents/{refresh_intent_id}"
            assert refresh_intent.params.link_token == link_token

        link_token = "test_link_token"
        refresh_intent_id = "test_refresh_intent_id"

        # Test using the resource
        link = self.fintoc.links.get(link_token)
        refresh_intent = link.refresh_intents.get(refresh_intent_id)
        assert_refresh_intent(refresh_intent)

        # Test using directly the manager
        refresh_intent = self.fintoc.refresh_intents.get(
            refresh_intent_id, link_token=link_token
        )
        assert_refresh_intent(refresh_intent)

    def test_link_refresh_intent_create(self):
        """Test creating a refresh intent for a link."""

        def assert_refresh_intent(refresh_intent):
            assert refresh_intent.method == "post"
            assert refresh_intent.url == "v1/refresh_intents"
            assert refresh_intent.json.refresh_type == "only_last"
            # Check link_token in either params or json
            assert (
                hasattr(refresh_intent.json, "link_token")
                and refresh_intent.json.link_token == link_token
            ) or (
                hasattr(refresh_intent.params, "link_token")
                and refresh_intent.params.link_token == link_token
            )

        link_token = "test_link_token"

        # Test using the resource
        link = self.fintoc.links.get(link_token)
        refresh_intent = link.refresh_intents.create(refresh_type="only_last")
        assert_refresh_intent(refresh_intent)

        # Test using directly the manager
        refresh_intent = self.fintoc.refresh_intents.create(
            refresh_type="only_last", link_token=link_token
        )
        assert_refresh_intent(refresh_intent)

    def test_charges_list(self):
        """Test getting all charges."""
        charges = list(self.fintoc.charges.list())

        assert len(charges) > 0
        for charge in charges:
            assert charge.method == "get"
            assert charge.url == "v1/charges"

    def test_charge_get(self):
        """Test getting a specific charge."""
        charge_id = "test_charge_id"

        charge = self.fintoc.charges.get(charge_id)

        assert charge.method == "get"
        assert charge.url == f"v1/charges/{charge_id}"

    def test_charge_create(self):
        """Test creating a charge."""
        charge_data = {
            "amount": 1000,
            "currency": "CLP",
            "payment_method": "bank_transfer",
        }

        charge = self.fintoc.charges.create(**charge_data)

        assert charge.method == "post"
        assert charge.url == "v1/charges"
        assert charge.json.amount == charge_data["amount"]
        assert charge.json.currency == charge_data["currency"]
        assert charge.json.payment_method == charge_data["payment_method"]

    def test_payment_intents_list(self):
        """Test getting all payment intents."""
        payment_intents = list(self.fintoc.payment_intents.list())

        assert len(payment_intents) > 0
        for payment_intent in payment_intents:
            assert payment_intent.method == "get"
            assert payment_intent.url == "v1/payment_intents"

    def test_payment_intent_get(self):
        """Test getting a specific payment intent."""
        payment_intent_id = "test_payment_intent_id"

        payment_intent = self.fintoc.payment_intents.get(payment_intent_id)

        assert payment_intent.method == "get"
        assert payment_intent.url == f"v1/payment_intents/{payment_intent_id}"

    def test_payment_intent_create(self):
        """Test creating a payment intent."""
        payment_intent_data = {
            "amount": 1000,
            "currency": "CLP",
            "payment_method": "bank_transfer",
        }

        payment_intent = self.fintoc.payment_intents.create(**payment_intent_data)

        assert payment_intent.method == "post"
        assert payment_intent.url == "v1/payment_intents"
        assert payment_intent.json.amount == payment_intent_data["amount"]
        assert payment_intent.json.currency == payment_intent_data["currency"]
        assert (
            payment_intent.json.payment_method == payment_intent_data["payment_method"]
        )

    def test_subscription_intents_list(self):
        """Test getting all subscription intents."""
        subscription_intents = list(self.fintoc.subscription_intents.list())

        assert len(subscription_intents) > 0
        for subscription_intent in subscription_intents:
            assert subscription_intent.method == "get"
            assert subscription_intent.url == "v1/subscription_intents"

    def test_subscription_intent_get(self):
        """Test getting a specific subscription intent."""
        subscription_intent_id = "test_subscription_intent_id"

        subscription_intent = self.fintoc.subscription_intents.get(
            subscription_intent_id
        )

        assert subscription_intent.method == "get"
        assert (
            subscription_intent.url
            == f"v1/subscription_intents/{subscription_intent_id}"
        )

    def test_subscription_intent_create(self):
        """Test creating a subscription intent."""
        subscription_intent_data = {"amount": 1000, "currency": "CLP"}

        subscription_intent = self.fintoc.subscription_intents.create(
            **subscription_intent_data
        )

        assert subscription_intent.method == "post"
        assert subscription_intent.url == "v1/subscription_intents"
        assert subscription_intent.json.amount == subscription_intent_data["amount"]
        assert subscription_intent.json.currency == subscription_intent_data["currency"]

    def test_webhook_endpoints_list(self):
        """Test getting all webhook endpoints."""
        webhook_endpoints = list(self.fintoc.webhook_endpoints.list())

        assert len(webhook_endpoints) > 0
        for webhook_endpoint in webhook_endpoints:
            assert webhook_endpoint.method == "get"
            assert webhook_endpoint.url == "v1/webhook_endpoints"

    def test_webhook_endpoint_get(self):
        """Test getting a specific webhook endpoint."""
        webhook_endpoint_id = "test_webhook_endpoint_id"

        webhook_endpoint = self.fintoc.webhook_endpoints.get(webhook_endpoint_id)

        assert webhook_endpoint.method == "get"
        assert webhook_endpoint.url == f"v1/webhook_endpoints/{webhook_endpoint_id}"

    def test_webhook_endpoint_create(self):
        """Test creating a webhook endpoint."""
        webhook_endpoint_data = {
            "url": "https://example.com/webhook",
            "enabled_events": ["movement.created", "link.updated"],
        }

        webhook_endpoint = self.fintoc.webhook_endpoints.create(**webhook_endpoint_data)

        assert webhook_endpoint.method == "post"
        assert webhook_endpoint.url == "v1/webhook_endpoints"
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
        assert webhook_endpoint.url == f"v1/webhook_endpoints/{webhook_endpoint_id}"
        assert webhook_endpoint.json.enabled_events == update_data["enabled_events"]

    def test_webhook_endpoint_delete(self):
        """Test deleting a webhook endpoint."""
        webhook_endpoint_id = "test_webhook_endpoint_id"

        result = self.fintoc.webhook_endpoints.delete(webhook_endpoint_id)

        assert result == webhook_endpoint_id

    def test_v2_accounts_list(self):
        """Test getting all accounts using v2 API."""
        accounts = list(self.fintoc.v2.accounts.list())

        assert len(accounts) > 0
        for account in accounts:
            assert account.method == "get"
            assert account.url == "v2/accounts"

    def test_v2_account_get(self):
        """Test getting a specific account using v2 API."""
        account_id = "test_account_id"

        account = self.fintoc.v2.accounts.get(account_id)

        assert account.method == "get"
        assert account.url == f"v2/accounts/{account_id}"

    def test_v2_account_create(self):
        """Test creating an account using v2 API."""
        account_data = {"description": "New test account"}

        account = self.fintoc.v2.accounts.create(**account_data)

        assert account.method == "post"
        assert account.url == "v2/accounts"
        assert account.json.description == account_data["description"]

    def test_v2_account_numbers_list(self):
        """Test getting all account numbers using v2 API."""
        account_id = "test_account_id"
        account_numbers = list(
            self.fintoc.v2.account_numbers.list(account_id=account_id)
        )

        assert len(account_numbers) > 0
        for account_number in account_numbers:
            assert account_number.method == "get"
            assert account_number.url == "v2/account_numbers"
            assert account_number.params.account_id == account_id

    def test_v2_account_number_get(self):
        """Test getting a specific account number using v2 API."""
        account_number_id = "test_account_number_id"

        account_number = self.fintoc.v2.account_numbers.get(account_number_id)

        assert account_number.method == "get"
        assert account_number.url == f"v2/account_numbers/{account_number_id}"

    def test_v2_account_number_create(self):
        """Test creating an account number using v2 API."""
        account_id = "test_account_id"

        description = "Test account number"
        metadata = {"test_key": "test_value"}

        account_number = self.fintoc.v2.account_numbers.create(
            account_id=account_id, description=description, metadata=metadata
        )

        assert account_number.method == "post"
        assert account_number.url == "v2/account_numbers"
        assert account_number.json.description == description
        assert account_number.json.metadata.test_key == metadata["test_key"]
        assert account_number.json.account_id == account_id

    def test_v2_account_number_update(self):
        """Test updating an account number using v2 API."""
        account_number_id = "test_account_number_id"
        metadata = {"test_key": "test_value"}

        account_number = self.fintoc.v2.account_numbers.update(
            account_number_id, metadata=metadata
        )

        assert account_number.method == "patch"
        assert account_number.url == f"v2/account_numbers/{account_number_id}"
        assert account_number.json.metadata.test_key == metadata["test_key"]

    def test_v2_account_number_delete(self):
        """Test deleting an account number using v2 API."""
        account_number_id = "test_account_number_id"

        result = self.fintoc.v2.account_numbers.delete(account_number_id)

        assert result == account_number_id

    def test_v2_transfers_list(self):
        """Test getting all transfers using v2 API."""
        account_id = "test_account_id"
        transfers = list(self.fintoc.v2.transfers.list(account_id=account_id))

        assert len(transfers) > 0
        for transfer in transfers:
            assert transfer.method == "get"
            assert transfer.url == "v2/transfers"
            assert transfer.params.account_id == account_id

    def test_v2_transfer_get(self):
        """Test getting a specific transfer using v2 API."""
        transfer_id = "test_transfer_id"

        transfer = self.fintoc.v2.transfers.get(transfer_id)

        assert transfer.method == "get"
        assert transfer.url == f"v2/transfers/{transfer_id}"

    def test_v2_transfer_create(self):
        """Test creating a transfer using v2 API."""
        account_id = "test_account_id"
        amount = 10000
        currency = "MXN"
        description = "Test transfer"
        metadata = {"test_key": "test_value"}

        transfer = self.fintoc.v2.transfers.create(
            account_id=account_id,
            amount=amount,
            currency=currency,
            description=description,
            metadata=metadata,
        )

        assert transfer.method == "post"
        assert transfer.url == "v2/transfers"
        assert transfer.json.amount == amount
        assert transfer.json.currency == currency
        assert transfer.json.description == description
        assert transfer.json.metadata.test_key == metadata["test_key"]

        idempotency_key_header = getattr(transfer.headers, "idempotency-key")
        assert idempotency_key_header is not None and idempotency_key_header != ""

        idempotency_key = "123456"
        transfer = self.fintoc.v2.transfers.create(
            account_id=account_id,
            amount=amount,
            currency=currency,
            description=description,
            metadata=metadata,
            idempotency_key=idempotency_key,
        )
        idempotency_key_header = getattr(transfer.headers, "idempotency-key")
        assert idempotency_key_header == "123456"

    def test_v2_simulate_receive_transfer(self):
        """Test simulating receiving a transfer using v2 API."""
        account_number_id = "test_account_number_id"
        amount = 10000
        currency = "MXN"

        transfer = self.fintoc.v2.simulate.receive_transfer(
            account_number_id=account_number_id, amount=amount, currency=currency
        )

        assert transfer.method == "post"
        assert transfer.url == "v2/simulate/receive_transfer"
        assert transfer.json.amount == amount
        assert transfer.json.currency == currency
        assert transfer.json.account_number_id == account_number_id


if __name__ == "__main__":
    pytest.main()
