"""Module to hold the webhook_endpoints manager."""

from fintoc.mixins import ManagerMixin


class WebhookEndpointsManager(ManagerMixin):

    """Represents a webhook_endpoints manager."""

    resource = "webhook_endpoint"
    methods = ["list", "get", "create", "update", "delete", "test"]

    def _test(self, identifier, **kwargs):
        """Send a test event to a webhook endpoint."""
        path = f"{self._build_path(**kwargs)}/{identifier}/test"
        return self._create(path_=path, **kwargs)
