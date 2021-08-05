"""
Core module to house the Client object of the Fintoc Python SDK.
"""

from fintoc.constants import API_BASE_URL, API_VERSION
from fintoc.managers import LinksManager, WebhookEndpointsManager
from fintoc.version import __version__


class Client:

    """Encapsulates the client behaviour and methods."""

    def __init__(self, api_key):
        self.data = ClientData(
            base_url=f"{API_BASE_URL}/{API_VERSION}",
            api_key=api_key,
            user_agent=f"fintoc-python/{__version__}",
        )
        self.links = LinksManager("/links", self.data)
        self.webhook_endpoints = WebhookEndpointsManager(
            "/webhook_endpoints", self.data
        )


class ClientData:
    def __init__(self, base_url, api_key, user_agent, params={}):
        self.base_url = base_url
        self.api_key = api_key
        self.user_agent = user_agent
        self.params = params

    @property
    def headers(self):
        return {"Authorization": self.api_key, "User-Agent": self.user_agent}

    def extend(
        self,
        base_url=None,
        api_key=None,
        user_agent=None,
        params=None,
    ):
        return ClientData(
            base_url=base_url or self.base_url,
            api_key=api_key or self.api_key,
            user_agent=user_agent or self.user_agent,
            params=params or self.params,
        )
