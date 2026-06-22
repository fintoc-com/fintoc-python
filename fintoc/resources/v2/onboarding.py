"""Module to hold the Onboarding resource."""

from fintoc.mixins import ResourceMixin


class Onboarding(ResourceMixin):
    """Represents a Fintoc Onboarding."""

    mappings = {
        "shareholders": "onboarding_shareholder",
        "documents": "onboarding_document",
    }
