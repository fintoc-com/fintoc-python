"""Module to hold the transfer batches manager."""

from fintoc.mixins import ManagerMixin


class TransferBatchesManager(ManagerMixin):
    """Represents a transfer batches manager."""

    resource = "transfer_batch"
    methods = ["list", "get", "create"]
