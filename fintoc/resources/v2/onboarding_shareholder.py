"""Module to hold the OnboardingShareholder resource."""

from fintoc.mixins import ResourceMixin


class OnboardingShareholder(ResourceMixin):
    """Represents a Fintoc Onboarding Shareholder."""

    mappings = {"document": "onboarding_document"}
