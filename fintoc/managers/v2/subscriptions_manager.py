"""Module to hold the subscriptions manager."""

from fintoc.mixins import ManagerMixin


class SubscriptionsManager(ManagerMixin):
    """Represents a subscriptions manager."""

    resource = "subscription"
    methods = ["list", "get", "cancel"]

    def _cancel(self, identifier, **kwargs):
        """Cancel a subscription."""
        path = f"{self._build_path(**kwargs)}/{identifier}/cancel"
        return self._create(path_=path, **kwargs)
