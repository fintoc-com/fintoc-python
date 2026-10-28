"""Module to hold the payment methods manager."""

from fintoc.mixins import ManagerMixin
from fintoc.utils import build_file_payload, can_raise_fintoc_error


class PaymentMethodsManager(ManagerMixin):
    """Represents a payment methods manager."""

    resource = "payment_method"
    methods = ["list", "get", "create", "cancel", "mandate_document"]

    file_parameters = ("consent_documents",)

    @can_raise_fintoc_error
    def _create(self, idempotency_key=None, path_=None, **kwargs):
        """Create a payment method as multipart, with bracket-nested fields."""
        if path_:
            return super()._create(
                idempotency_key=idempotency_key, path_=path_, **kwargs
            )
        data, files = [], []
        for key, value in kwargs.items():
            self._flatten(key, value, data, files)
        return self._upload(
            self._build_path(**kwargs),
            files,
            method="post",
            data=dict(data),
            idempotency_key=idempotency_key,
        )

    def _cancel(self, identifier, **kwargs):
        """Cancel a payment method."""
        path = f"{self._build_path(**kwargs)}/{identifier}/cancel"
        return self._create(path_=path, **kwargs)

    def _mandate_document(self, identifier, **kwargs):
        """Get a temporary URL to download the signed mandate contract."""
        path = f"{self._build_path(**kwargs)}/{identifier}/mandate_document"
        return self._request_resource(
            "get", path, resource="mandate_document", **kwargs
        )

    def _flatten(self, key, value, data, files, is_file=False):
        """Flatten a nested parameter into multipart form fields and files."""
        if value is None:
            return
        if isinstance(value, dict):
            for nested_key, nested_value in value.items():
                self._flatten(
                    f"{key}[{nested_key}]",
                    nested_value,
                    data,
                    files,
                    is_file=is_file or nested_key in self.file_parameters,
                )
        elif is_file:
            filename = key.rsplit("[", 1)[-1].rstrip("]")
            files.append((key, build_file_payload(value, default_filename=filename)))
        else:
            data.append((key, str(value)))
