"""Tests for the JWS signature generation."""

import base64
import json
import time

import pytest
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa

from fintoc.jws import JWSSignature


@pytest.fixture(name="private_key")
def fixture_private_key():
    """Generate a test RSA private key."""
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    return pem


@pytest.fixture(name="private_key_file")
def fixture_private_key_file(private_key, tmp_path):
    """Create a temporary file with the test private key."""
    key_path = tmp_path / "private_key.pem"
    key_path.write_bytes(private_key)
    return key_path


class TestJWSSignature:
    """Test cases for JWSSignature class."""

    def test_init_with_string(self, private_key):
        """Test initializing with PEM string."""
        jws = JWSSignature(private_key.decode())
        assert jws.private_key is not None

    def test_init_with_bytes(self, private_key):
        """Test initializing with PEM bytes."""
        jws = JWSSignature(private_key)
        assert jws.private_key is not None

    def test_init_with_path_string(self, private_key_file):
        """Test initializing with path as string."""
        jws = JWSSignature(str(private_key_file))
        assert jws.private_key is not None

    def test_init_with_path_object(self, private_key_file):
        """Test initializing with Path object."""
        jws = JWSSignature(private_key_file)
        assert jws.private_key is not None

    def test_init_with_invalid_type(self):
        """Test initializing with invalid type raises ValueError."""
        with pytest.raises(ValueError):
            JWSSignature(123)

    def test_init_with_invalid_path(self):
        """Test initializing with non-existent file path."""
        with pytest.raises(ValueError):
            JWSSignature("nonexistent.pem")

    def test_init_with_invalid_key_format(self):
        """Test initializing with invalid key format."""
        with pytest.raises(ValueError):
            JWSSignature("not a valid key")

    def test_generate_header_with_dict(self, private_key):
        """Test generating header with dict payload."""
        jws = JWSSignature(private_key)
        payload = {"amount": 1000, "currency": "CLP"}
        header = jws.generate_header(payload)

        parts = header.split(".")
        assert len(parts) == 2

        protected = json.loads(
            base64.urlsafe_b64decode(parts[0] + "=" * (4 - len(parts[0]) % 4)).decode()
        )

        assert protected["alg"] == "RS256"
        assert "nonce" in protected
        assert "ts" in protected
        assert protected["crit"] == ["ts", "nonce"]

    def test_generate_header_with_string(self, private_key):
        """Test generating header with string payload."""
        jws = JWSSignature(private_key)
        payload = json.dumps({"amount": 1000, "currency": "CLP"})
        header = jws.generate_header(payload)

        parts = header.split(".")
        assert len(parts) == 2

        protected = json.loads(
            base64.urlsafe_b64decode(parts[0] + "=" * (4 - len(parts[0]) % 4)).decode()
        )

        assert protected["alg"] == "RS256"
        assert "nonce" in protected
        assert "ts" in protected
        assert protected["crit"] == ["ts", "nonce"]

    def test_header_verification(self, private_key):
        """Test that generated headers can be verified."""
        jws = JWSSignature(private_key)
        payload = {"amount": 1000, "currency": "CLP"}
        header = jws.generate_header(payload)

        protected_b64, signature_b64 = header.split(".")
        payload_b64 = (
            base64.urlsafe_b64encode(json.dumps(payload).encode()).rstrip(b"=").decode()
        )
        signing_input = f"{protected_b64}.{payload_b64}"
        signature = base64.urlsafe_b64decode(
            signature_b64 + "=" * (4 - len(signature_b64) % 4)
        )

        public_key = serialization.load_pem_private_key(
            private_key, password=None
        ).public_key()

        # This should not raise an exception
        public_key.verify(
            signature, signing_input.encode(), padding.PKCS1v15(), hashes.SHA256()
        )

    def test_timestamp_is_current(self, private_key):
        """Test that generated timestamp is current."""
        jws = JWSSignature(private_key)
        payload = {"test": "data"}
        header = jws.generate_header(payload)

        protected_b64 = header.split(".")[0]
        protected = json.loads(
            base64.urlsafe_b64decode(
                protected_b64 + "=" * (4 - len(protected_b64) % 4)
            ).decode()
        )

        assert abs(protected["ts"] - int(time.time())) < 10

    def test_nonce_is_random(self, private_key):
        """Test that nonce is random for each call."""
        jws = JWSSignature(private_key)
        payload = {"test": "data"}

        header1 = jws.generate_header(payload)
        header2 = jws.generate_header(payload)

        protected1 = json.loads(
            base64.urlsafe_b64decode(header1.split(".")[0] + "====").decode()
        )
        protected2 = json.loads(
            base64.urlsafe_b64decode(header2.split(".")[0] + "====").decode()
        )

        assert protected1["nonce"] != protected2["nonce"]
