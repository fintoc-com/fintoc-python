class FintocError(Exception):
    def __init__(self, error_data):
        super().__init__(error_data["message"])
        self.code = error_data["code"]


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
