"""Module to hold the refresh_intents manager."""

from fintoc.managers._link_token_manager import LinkTokenManager


class RefreshIntentsManager(LinkTokenManager):

    """Represents a refresh_intents manager."""

    resource = "refresh_intent"
    methods = ["all", "get", "create"]
