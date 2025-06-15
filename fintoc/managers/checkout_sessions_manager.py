"""Module to hold the checkout sessions manager."""

from fintoc.mixins import ManagerMixin


class CheckoutSessionsManager(ManagerMixin):
    """Represents a checkout sessions manager."""

    resource = "checkout_session"
    methods = ["create", "get", "expire"]

    def _expire(self, identifier, **kwargs):
        """Expire a checkout session."""
        path = f"{self._build_path(**kwargs)}/{identifier}/expire"
        return self._create(path_=path, **kwargs)
