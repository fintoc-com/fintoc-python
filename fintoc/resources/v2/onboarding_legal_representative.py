"""Module to hold the OnboardingLegalRepresentative resource."""

from fintoc.mixins import ResourceMixin


class OnboardingLegalRepresentative(ResourceMixin):
    """Represents a Fintoc Onboarding Legal Representative."""

    mappings = {"documents": "onboarding_document"}
