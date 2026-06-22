"""Module to hold the onboardings manager."""

import mimetypes
import os

from fintoc.mixins import ManagerMixin
from fintoc.resource_handlers import resource_upload
from fintoc.utils import can_raise_fintoc_error, get_resource_class


class OnboardingsManager(ManagerMixin):
    """Represents an onboardings manager."""

    resource = "onboarding"
    methods = [
        "list",
        "get",
        "create",
        "submit",
        "upload_document",
        "upload_shareholder_document",
    ]

    def _submit(self, identifier, **kwargs):
        """Submit an onboarding for review."""
        path = f"{self._build_path(**kwargs)}/{identifier}/submit"
        return self._create(path_=path, **kwargs)

    def _upload_document(self, identifier, slot_key, file, **kwargs):
        """Upload a document to a slot, identified by :slot_key:."""
        path = f"{self._build_path(**kwargs)}/{identifier}/documents/{slot_key}"
        return self._upload(path, file)

    def _upload_shareholder_document(self, identifier, shareholder_id, file, **kwargs):
        """Upload a document for a shareholder of an onboarding."""
        path = (
            f"{self._build_path(**kwargs)}/{identifier}"
            f"/shareholders/{shareholder_id}/document"
        )
        return self._upload(path, file)

    @can_raise_fintoc_error
    def _upload(self, path, file):
        """Perform a multipart ``PUT`` upload of :file: and objetize the result."""
        klass = get_resource_class(self.__class__.resource)
        files = {"file": self._build_file_payload(file)}
        return resource_upload(
            self._client, path, klass, self._handlers, self.__class__.methods, files
        )

    @staticmethod
    def _build_file_payload(file):
        """
        Build the ``(filename, fileobj, content_type)`` tuple expected by httpx
        from either a path (``str`` / ``os.PathLike``) or a binary file-like
        object.
        """
        if isinstance(file, (str, os.PathLike)):
            filename = os.path.basename(os.fspath(file))
            content_type = mimetypes.guess_type(filename)[0]
            return (filename, open(file, "rb"), content_type)  # noqa: SIM115

        filename = os.path.basename(getattr(file, "name", "") or "") or None
        content_type = mimetypes.guess_type(filename)[0] if filename else None
        return (filename, file, content_type)
