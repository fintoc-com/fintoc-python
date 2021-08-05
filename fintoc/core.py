"""
Core module to house the Client object of the Fintoc Python SDK.
"""

from fintoc.managers.links_manager import LinksManager
from fintoc.version import __version__


class Client:

    """Encapsulates the client behaviour and methods."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.user_agent = f"fintoc-python/{__version__}"
        self.headers = {"Authorization": self.api_key, "User-Agent": self.user_agent}
        self.links = LinksManager("/links", self.headers)
