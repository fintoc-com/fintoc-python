"""Module to hold the payout resources manager."""

from fintoc.mixins import ManagerMixin
from fintoc.resource_handlers import resource_list
from fintoc.utils import can_raise_fintoc_error, get_resource_class


class PayoutResourcesManager(ManagerMixin):

    """Represents a payout resources manager."""

    resource = "generic_fintoc_resource"
    methods = ["list"]

    resource_types = {
        "payment_intent": "payment_intent",
        "charge": "charge",
        "refund": "refund",
        "refund_adjustment": "refund",
    }

    @can_raise_fintoc_error
    def _list(self, **kwargs):
        """List the resources of a payout of the given ``resource_type``."""
        resource = self.resource_types.get(
            kwargs.get("resource_type"), self.__class__.resource
        )
        return resource_list(
            client=self._client,
            path=self._build_path(**kwargs),
            klass=get_resource_class(resource),
            handlers={},
            methods=[],
            params=kwargs,
        )
