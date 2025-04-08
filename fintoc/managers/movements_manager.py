"""Module to hold the movements manager."""

from fintoc.managers._link_token_manager import LinkTokenManager


class MovementsManager(LinkTokenManager):

    """Represents a movements manager."""

    resource = "movement"
    methods = ["all", "get"]
