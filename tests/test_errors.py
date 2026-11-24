import pytest

from fintoc.errors import (
    ApiError,
    AuthenticationError,
    FintocError,
    InstitutionError,
    InvalidRequestError,
    LinkError,
    WebhookSignatureError,
)


class TestFintocError:
    def test_complete_error_data(self):
        error_data = {
            "type": "invalid_request_error",
            "code": "invalid_param",
            "message": "The param 'amount' is required.",
            "param": "amount",
            "doc_url": "https://docs.fintoc.com/errors/invalid_param",
        }
        err = FintocError(error_data)
        assert isinstance(err, Exception)
        assert "invalid_request_error: invalid_param (amount)" in str(err)
        assert "The param 'amount' is required." in str(err)
        assert "Check the docs for more info: https://docs.fintoc.com" in str(err)

    def test_minimal_error_data(self):
        error_data = {
            "type": "api_error",
        }
        err = FintocError(error_data)
        assert str(err) == "api_error"

    def test_missing_type_does_not_raise_type_error(self):
        error_data = {
            "message": "Server encountered an unknown error.",
        }
        err = FintocError(error_data)
        assert "error" in str(err)
        assert "Server encountered an unknown error." in str(err)

    def test_error_subclasses_inherit_fintoc_error(self):
        subclasses = [
            ApiError,
            AuthenticationError,
            LinkError,
            InstitutionError,
            InvalidRequestError,
        ]
        for cls in subclasses:
            err = cls({"type": "test_error", "message": "msg"})
            assert isinstance(err, FintocError)
            assert isinstance(err, Exception)

    def test_webhook_signature_error(self):
        err = WebhookSignatureError("Invalid signature")
        assert isinstance(err, Exception)
        assert str(err) == "Invalid signature"
