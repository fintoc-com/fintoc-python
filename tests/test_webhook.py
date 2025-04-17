from datetime import datetime, timedelta, timezone

import httpx
import pytest
from freezegun import freeze_time

from fintoc.errors import WebhookSignatureError
from fintoc.webhook import WebhookSignature

# Test constants from the real webhook
SECRET = "whsec_test_secret"
PAYLOAD = """
{
  "id": "evt_2AaZeLCz0GjOW5zj",
  "type": "payment_intent.succeeded",
  "mode": "test",
  "created_at": "2025-04-05T21:57:31.834Z",
  "data": {
    "id": "pi_2vKOKniSGXRhXTKrJ67VXZxGCVt",
    "mode": "test",
    "amount": 1,
    "object": "payment_intent",
    "status": "succeeded",
    "currency": "MXN",
    "metadata": {},
    "created_at": "2025-04-05T21:57:17Z",
    "expires_at": null,
    "error_reason": null,
    "payment_type": "bank_transfer",
    "reference_id": null,
    "widget_token": null,
    "customer_email": null,
    "sender_account": {
      "type": "checking_account",
      "number": "501514890244223279",
      "holder_id": "mfiu593501oe4",
      "institution_id": "mx_stp"
    },
    "business_profile": null,
    "transaction_date": null,
    "recipient_account": {
      "type": "checking_account",
      "number": "646180357600000000",
      "holder_id": "fsm211008hz9",
      "institution_id": "mx_stp"
    },
    "payment_type_options": {}
  },
  "object": "event"
}
"""

# Remove whitespace and line returns from PAYLOAD
PAYLOAD = "".join(PAYLOAD.split())

TIMESTAMP = 1743890251
HEADER = (
    f"t={TIMESTAMP},v1=11b98dd8f5500109246aa4d9875fad2e97d462560b012a5f50ff924411de0b0f"
)
SIGNATURE_DATETIME = datetime.fromtimestamp(TIMESTAMP, tz=timezone.utc)


class TestWebhookSignature:
    @freeze_time(SIGNATURE_DATETIME)
    def test_valid_signature(self):
        assert (
            WebhookSignature.verify_header(
                payload=PAYLOAD, header=HEADER, secret=SECRET
            )
            is True
        )

    @freeze_time(SIGNATURE_DATETIME)
    def test_invalid_secret(self):
        """Test that an incorrect secret key fails verification"""
        with pytest.raises(WebhookSignatureError, match="Signature mismatch"):
            WebhookSignature.verify_header(
                payload=PAYLOAD, header=HEADER, secret="whsec_wrong_secret"
            )

    @freeze_time(SIGNATURE_DATETIME)
    def test_modified_payload(self):
        """Test that a modified payload fails verification"""
        modified_payload = PAYLOAD.replace(
            "payment_intent.succeeded", "payment_intent.failed"
        )

        with pytest.raises(WebhookSignatureError, match="Signature mismatch"):
            WebhookSignature.verify_header(
                payload=modified_payload, header=HEADER, secret=SECRET
            )

        # Should fail with no tolerance
        with pytest.raises(WebhookSignatureError, match="Signature mismatch"):
            WebhookSignature.verify_header(
                payload=modified_payload, header=HEADER, secret=SECRET, tolerance=None
            )

    def test_malformed_header(self):
        malformed_headers = [
            "",
            "invalid_format",
            "t=1743890251",
            "v1=11b98dd8f5500109246aa4d9875fad2e97d462560b012a5f50ff924411de0b0f",
            "t=invalid,v1=11b98dd8f5500109246aa4d9875fad2e97d462560b012a5f50ff924411de0b0f",  # noqa: E501
        ]

        for header in malformed_headers:
            with pytest.raises(WebhookSignatureError):
                WebhookSignature.verify_header(
                    payload=PAYLOAD, header=header, secret=SECRET
                )

    @freeze_time(SIGNATURE_DATETIME)
    def test_header_contains_valid_signature(self):
        header = HEADER + ",v2=bad_signature"
        assert (
            WebhookSignature.verify_header(
                payload=PAYLOAD, header=header, secret=SECRET
            )
            is True
        )

    def test_timestamp_validation(self):
        # Should pass with custom tolerance and timestamp on
        with freeze_time(SIGNATURE_DATETIME + timedelta(seconds=500)):
            assert (
                WebhookSignature.verify_header(
                    payload=PAYLOAD, header=HEADER, secret=SECRET, tolerance=600
                )
                is True
            )

        # Should pass with default tolerance and timestamp on
        with freeze_time(SIGNATURE_DATETIME + timedelta(seconds=200)):
            assert (
                WebhookSignature.verify_header(
                    payload=PAYLOAD, header=HEADER, secret=SECRET
                )
                is True
            )

        # Should fail with default tolerance and timestamp off
        with freeze_time(SIGNATURE_DATETIME + timedelta(seconds=400)):
            with pytest.raises(
                WebhookSignatureError, match="Timestamp outside the tolerance zone"
            ):
                WebhookSignature.verify_header(
                    payload=PAYLOAD,
                    header=HEADER,
                    secret=SECRET,
                )

        # Should fail with custom tolerance and timestamp off
        with freeze_time(SIGNATURE_DATETIME + timedelta(seconds=100)):
            with pytest.raises(
                WebhookSignatureError, match="Timestamp outside the tolerance zone"
            ):
                WebhookSignature.verify_header(
                    payload=PAYLOAD, header=HEADER, secret=SECRET, tolerance=10
                )

        # Should pass with no tolerance and timestamp off
        with freeze_time(SIGNATURE_DATETIME + timedelta(seconds=10100)):
            WebhookSignature.verify_header(
                payload=PAYLOAD, header=HEADER, secret=SECRET, tolerance=None
            )

    def test_empty_values(self):
        """Test handling of empty values"""
        with pytest.raises(WebhookSignatureError):
            WebhookSignature.verify_header(payload=PAYLOAD, header="", secret=SECRET)

        with pytest.raises(WebhookSignatureError):
            WebhookSignature.verify_header(payload="", header=HEADER, secret=SECRET)

        with pytest.raises(WebhookSignatureError):
            WebhookSignature.verify_header(payload=PAYLOAD, header=HEADER, secret="")
