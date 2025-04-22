"""
Module to hold all the fixtures and stuff that needs to get auto-imported
by PyTest.
"""

import json
from json.decoder import JSONDecodeError

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


@pytest.fixture
def patch_http_client(monkeypatch):
    class MockResponse:
        def __init__(self, method, base_url, url, params, json, headers):
            self._base_url = base_url
            self._params = params
            page = None
            if method == "get" and url[-1] == "s":
                page = int(self._params.pop("page", 1))
            self._page = page
            self._method = method
            self._url = url
            self._json = json
            self._headers = headers

            # Extract the ID from the URL if it's a specific resource request
            self._id = None
            if "/" in url and not url.endswith("s"):
                self._id = url.split("/")[-1]

        @property
        def headers(self):
            resp_headers = dict(self._headers)
            if self._page is not None and self._page < 10:
                params = "&".join([*self.formatted_params, f"page={self._page + 1}"])
                url = self._url.lstrip("/")
                resp_headers["link"] = (
                    f"<{self._base_url}/{url}?{params}>; " 'rel="next"'
                )
            return resp_headers

        @property
        def formatted_params(self):
            return [f"{k}={v}" for k, v in self._params.items()]

        def raise_for_status(self):
            pass

        def json(self):
            if self._method == "delete":
                raise JSONDecodeError("Expecting value", "doc", 0)
            if self._method == "get" and self._url[-1] == "s":
                return [
                    {
                        "id": "idx",
                        "method": self._method,
                        "url": self._url,
                        "params": self._params,
                        "json": self._json,
                        "page": self._page,
                        "headers": self.headers,
                    }
                    for _ in range(10)
                ]
            return {
                # Use the ID from the URL if available, otherwise use "idx"
                "id": self._id if self._id else "idx",
                "method": self._method,
                "url": self._url,
                "params": self._params,
                "json": self._json,
                "headers": self.headers,
            }

    class MockClient(httpx.Client):
        def send(self, request: httpx.Request, **_kwargs):
            query_string = request.url.query.decode("utf-8")
            query = query_string.split("&") if query_string else []
            inner_params = {y[0]: y[1] for y in (x.split("=") for x in query)}
            complete_params = {
                **inner_params,
                **({} if request.url.params is None else request.url.params),
            }
            usable_url = request.url.path
            raw_body = request.content.decode("utf-8")
            return MockResponse(
                request.method.lower(),
                self.base_url,
                usable_url.lstrip("/"),
                complete_params,
                json.loads(raw_body) if raw_body else None,
                request.headers,
            )

    monkeypatch.setattr(httpx, "Client", MockClient)

    from fintoc.client import Client

    mock_client = MockClient()
    monkeypatch.setattr(Client, "_client", mock_client)
