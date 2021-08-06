from fintoc.mixins import ManagerMixin


class SubscriptionsManager(ManagerMixin):
    resource = "subscriptions"
    methods = ["all", "get"]
