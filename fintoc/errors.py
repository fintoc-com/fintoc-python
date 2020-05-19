"""
errors.py
=========

A module with several errors you can encounter using Fintoc.
"""


class FintocError(Exception):
    def __init__(self, error):
        super().__init__()
        self.message = error.get("message")
        self.doc_url = error.get("doc_url") or "https://fintoc.com/docs"

    def __str__(self):
        return f"\n{self.message}" f"\nPlease check the docs at: {self.doc_url}"


class InvalidRequestError(FintocError):
    pass


class LinkError(FintocError):
    pass


class AuthenticationError(FintocError):
    pass


class InstitutionError(FintocError):
    pass


class ApiError(FintocError):
    pass


class MissingResourceError(InvalidRequestError):
    pass


class InvalidLinkTokenError(InvalidRequestError):
    pass


class InvalidUsernameError(InvalidRequestError):
    pass


class InvalidHolderTypeError(InvalidRequestError):
    pass


class MissingParameterError(InvalidRequestError):
    pass


class EmptyStringError(InvalidRequestError):
    pass


class UnrecognizedRequestError(InvalidRequestError):
    pass


class InvalidDateError(InvalidRequestError):
    pass


class InvalidCredentialsError(LinkError):
    pass


class LockedCredentialsError(LinkError):
    pass


class InvalidApiKeyError(AuthenticationError):
    pass


class UnavailableInstitutionError(InstitutionError):
    pass


class InternalServerError(ApiError):
    pass
