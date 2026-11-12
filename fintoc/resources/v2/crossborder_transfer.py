"""Module to hold the Crossborder Transfer resource."""

from fintoc.mixins import ResourceMixin


class CrossborderTransfer(ResourceMixin):
    """Represents a Fintoc Crossborder Transfer."""

    mappings = {"beneficiary": "crossborder_beneficiary"}
