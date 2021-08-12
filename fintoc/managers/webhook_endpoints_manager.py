"""Module to hold the webhook_endpoints manager."""

from fintoc.mixins import ManagerMixin


class WebhookEndpointsManager(ManagerMixin):

    """Represents a webhook_endpoints manager."""

    resource = "webhook_endpoint"
    methods = ["all", "get", "create", "update", "delete"]
