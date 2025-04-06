"""Module to handle JWS signature generation for Fintoc API requests."""

import base64
import json
import os
import secrets
import time
from pathlib import Path
from typing import Union

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


class JWSSignature:
    """Class to handle JWS signature generation for Fintoc API requests."""

    def __init__(self, private_key: Union[str, bytes, Path]):
        """
        Initialize the JWSSignature with a private key.

        Args:
            private_key: The RSA private key in one of these formats:
                - String containing PEM-formatted key
                - Bytes containing PEM-formatted key
                - Path object or string path to a PEM key file

        Example:
            >>> # From a string
            >>> with open('private_key.pem', 'r') as f:
            ...     key_str = f.read()
            >>> jws = JWSSignature(key_str)
            >>>
            >>> # From a file path
            >>> jws = JWSSignature('private_key.pem')
            >>>
            >>> # From environment variable
            >>> jws = JWSSignature(os.environ.get('PRIVATE_KEY'))
        """
        if isinstance(private_key, (str, Path)) and os.path.isfile(str(private_key)):
            with open(private_key, "rb") as key_file:
                private_key_bytes = key_file.read()
        elif isinstance(private_key, str):
            private_key_bytes = private_key.encode()
        elif isinstance(private_key, bytes):
            private_key_bytes = private_key
        else:
            raise ValueError(
                "private_key must be a PEM string, bytes, or a path to a key file"
            )

        self.private_key = serialization.load_pem_private_key(
            private_key_bytes, password=None
        )

    def generate_header(self, raw_body: Union[str, dict]) -> str:
        """
        Generate a JWS signature header for Fintoc API requests.

        Args:
            raw_body: The request body as a string or dict. If dict, it will be
            converted to JSON.

        Returns:
            str: The JWS signature header to be used in the 'Fintoc-JWS-Signature'
            header.

        Example:
            >>> jws = JWSSignature(private_key)
            >>> body = {"amount": 1000, "currency": "CLP"}
            >>> jws_header = jws.generate_header(body)
            >>> # Use in request headers:
            >>> headers = {
            ...     'Fintoc-JWS-Signature': jws_header,
            ...     'Authorization': 'Bearer sk_test...'
            ... }
        """
        if isinstance(raw_body, dict):
            raw_body = json.dumps(raw_body)

        headers = {
            "alg": "RS256",
            "nonce": secrets.token_hex(16),
            "ts": int(time.time()),
            "crit": ["ts", "nonce"],
        }

        protected_base64 = (
            base64.urlsafe_b64encode(json.dumps(headers).encode()).rstrip(b"=").decode()
        )
        payload_base64 = (
            base64.urlsafe_b64encode(raw_body.encode()).rstrip(b"=").decode()
        )
        signing_input = f"{protected_base64}.{payload_base64}"
        signature_raw = self.private_key.sign(
            signing_input.encode(), padding.PKCS1v15(), hashes.SHA256()
        )
        signature_base64 = base64.urlsafe_b64encode(signature_raw).rstrip(b"=").decode()

        return f"{protected_base64}.{signature_base64}"
