"""Module to hold the refunds manager."""

from fintoc.mixins import ManagerMixin


class RefundsManager(ManagerMixin):

    """Represents a refunds manager."""

    resource = "refund"
    methods = ["list", "get", "create", "cancel", "voucher_url"]

    def _cancel(self, identifier, **kwargs):
        """Expire a refund."""
        path = f"{self._build_path(**kwargs)}/{identifier}/cancel"
        return self._create(path_=path, **kwargs)

    def _voucher_url(self, identifier, **kwargs):
        """Get a presigned URL to download the PDF voucher of a refund."""
        path = f"{self._build_path(**kwargs)}/{identifier}/voucher_url"
        return self._request_resource("get", path, resource="voucher_url", **kwargs)
