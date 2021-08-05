from fintoc.mixins import ManagerMixin


class WebhookEndpointsManager(ManagerMixin):
    resource = "webhook_endpoint"
    methods = ["all", "get", "create", "update", "delete"]
