"""Module to hold the Fintoc custom errors."""


class FintocError(Exception):

    """Represents the base custom error."""

    def __init__(self, error_data):
        error_type = error_data.get("type")
        error_code = error_data.get("code")
        error_message = error_data.get("message")
        error_param = error_data.get("param")
        error_doc_url = error_data.get("doc_url")
        message = error_type
        message += f": {error_code}" if error_code is not None else ""
        message += f" ({error_param})" if error_param is not None else ""
        message += f"\n{error_message}"
        message += (
            f"\nCheck the docs for more info: {error_doc_url}"
            if error_doc_url is not None
            else ""
        )
        super().__init__(message)


class ApiError(FintocError):
    """Represents an error with the API server."""


class AuthenticationError(FintocError):
    """Represents an error with the authentication."""


class LinkError(FintocError):
    """Represents an error with a Link object."""


class InstitutionError(FintocError):
    """Represents an error with an Institution object."""


class InvalidRequestError(FintocError):
    """Represents an error because of an invalid request."""
