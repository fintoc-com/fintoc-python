"""
Module to hold all the fixtures and stuff that needs to get auto-imported
by PyTest.
"""

import httpx
import pytest


@pytest.fixture
def patch_http_error(monkeypatch):
    class MockResponse:
        def __init__(self):
            pass

        def json(self):
            return {
                "error": {
                    "type": "api_error",
                    "message": "This is a test error message",
                }
            }

    class MockHTTPError(httpx.HTTPError):
        def __init__(self, message):
            super().__init__(message)
            self.response = MockResponse()

    monkeypatch.setattr(httpx, "HTTPError", MockHTTPError)
