"""
Webhook signature validation module for Fintoc's webhooks.

This module provides functionality to verify webhook signatures using HMAC-SHA256,
following Fintoc's webhook validation specification. It ensures that webhooks
are authentic and haven't been tampered with during transmission.
"""

import hmac
import time
from hashlib import sha256
from typing import Dict, Optional, Tuple

from fintoc.errors import WebhookSignatureError


class WebhookSignature:
    """
    Handles webhook signature validation for Fintoc webhooks.
    """

    EXPECTED_SCHEME = "v1"
    DEFAULT_TOLERANCE = 300  # 5 minutes in seconds

    @staticmethod
    def verify_header(
        payload: str,
        header: str,
        secret: str,
        tolerance: Optional[int] = DEFAULT_TOLERANCE,
    ) -> bool:
        """
        Verify the webhook signature header.

        Args:
            payload: The raw request body as a string
            header: The Fintoc-Signature header value
            secret: The webhook secret key
            tolerance: Number of seconds to tolerate when checking timestamp

        Returns:
            bool: True if the signature is valid

        Raises:
            WebhookSignatureError: If the signature is invalid
        """
        timestamp, signatures = WebhookSignature._parse_header(header)

        if tolerance:
            WebhookSignature._verify_timestamp(timestamp, tolerance)

        expected_sig = WebhookSignature._compute_signature(
            payload=payload, timestamp=timestamp, secret=secret
        )

        # Get the v1 signature from parsed signatures
        signature = signatures.get(WebhookSignature.EXPECTED_SCHEME)
        if not signature:
            raise WebhookSignatureError(
                f"No {WebhookSignature.EXPECTED_SCHEME} signature found"
            )

        if not hmac.compare_digest(expected_sig, signature):
            raise WebhookSignatureError("Signature mismatch")

        return True

    @staticmethod
    def _parse_header(header: str) -> Tuple[int, Dict[str, str]]:
        """
        Parse the webhook signature header.

        Args:
            header: The Fintoc-Signature header value

        Returns:
            Tuple containing timestamp and dict of signature schemes

        Raises:
            WebhookSignatureError: If header format is invalid
        """
        try:
            pairs = dict(part.split("=", 1) for part in header.split(","))

            if "t" not in pairs:
                raise WebhookSignatureError("Missing timestamp in header")

            timestamp = int(pairs["t"])
            signatures = {k: v for k, v in pairs.items() if k != "t"}

            return timestamp, signatures

        except (ValueError, KeyError) as e:
            raise WebhookSignatureError(
                "Unable to extract timestamp and signatures from header"
            ) from e

    @staticmethod
    def _compute_signature(payload: str, timestamp: int, secret: str) -> str:
        """
        Compute the expected signature for a payload.

        Args:
            payload: The raw request body
            timestamp: Unix timestamp
            secret: Webhook secret key

        Returns:
            str: The computed signature
        """
        signed_payload = f"{timestamp}.{payload}"
        return hmac.new(
            secret.encode("utf-8"), signed_payload.encode("utf-8"), sha256
        ).hexdigest()

    @staticmethod
    def _verify_timestamp(timestamp: int, tolerance: int) -> None:
        """
        Verify that the timestamp is within tolerance.

        Args:
            timestamp: Unix timestamp to verify
            tolerance: Number of seconds to tolerate

        Raises:
            WebhookSignatureError: If timestamp is outside tolerance window
        """
        now = int(time.time())

        if timestamp < (now - tolerance):
            raise WebhookSignatureError(
                f"Timestamp outside the tolerance zone ({timestamp})"
            )
