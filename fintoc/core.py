"""
Core module to house the Fintoc object of the Fintoc Python SDK.
"""

from fintoc.client import Client
from fintoc.constants import API_BASE_URL, API_VERSION
from fintoc.managers import LinksManager, WebhookEndpointsManager
from fintoc.version import __version__


class Fintoc:

    """Encapsulates the core object's behaviour and methods."""

    def __init__(self, api_key):
        self._client = Client(
            base_url=f"{API_BASE_URL}/{API_VERSION}",
            api_key=api_key,
            user_agent=f"fintoc-python/{__version__}",
        )
        self.links = LinksManager("/links", self._client)
        self.webhook_endpoints = WebhookEndpointsManager(
            "/webhook_endpoints", self._client
        )
