"""Module to hold the Onboarding resource."""

from fintoc.mixins import ResourceMixin


class Onboarding(ResourceMixin):
    """Represents a Fintoc Onboarding."""

    mappings = {
        "legal_representatives": "onboarding_legal_representative",
        "shareholders": "onboarding_shareholder",
        "documents": "onboarding_document",
    }
