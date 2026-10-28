"""Module to hold the onboardings manager."""

from fintoc.mixins import ManagerMixin
from fintoc.utils import build_file_payload


class OnboardingsManager(ManagerMixin):
    """Represents an onboardings manager."""

    resource = "onboarding"
    methods = [
        "list",
        "get",
        "create",
        "submit",
        "upload_document",
        "append_document",
        "delete_document",
        "upload_shareholder_document",
        "upload_legal_representative_document",
    ]

    def _submit(self, identifier, **kwargs):
        """Submit an onboarding for review."""
        path = f"{self._build_path(**kwargs)}/{identifier}/submit"
        return self._create(path_=path, **kwargs)

    def _upload_document(self, identifier, slot_key, file, **kwargs):
        """Upload a document to a slot, replacing the one already there."""
        path = f"{self._build_path(**kwargs)}/{identifier}/documents/{slot_key}"
        return self._upload(path, {"file": self._build_file_payload(file)})

    def _append_document(self, identifier, slot_key, file, **kwargs):
        """Add a document to a multi-file slot, keeping the existing ones."""
        path = f"{self._build_path(**kwargs)}/{identifier}/documents/{slot_key}"
        return self._upload(
            path, {"file": self._build_file_payload(file)}, method="post"
        )

    def _delete_document(self, identifier, slot_key, document_id, **kwargs):
        """Delete a document from a slot."""
        path = (
            f"{self._build_path(**kwargs)}/{identifier}"
            f"/documents/{slot_key}/{document_id}"
        )
        return self._request_resource("delete", path, **kwargs)

    def _upload_shareholder_document(self, identifier, shareholder_id, file, **kwargs):
        """Upload a document for a shareholder of an onboarding."""
        path = (
            f"{self._build_path(**kwargs)}/{identifier}"
            f"/shareholders/{shareholder_id}/document"
        )
        return self._upload(path, {"file": self._build_file_payload(file)})

    def _upload_legal_representative_document(
        self, identifier, legal_representative_id, slot_key, file, **kwargs
    ):
        """Upload a document for a legal representative of an onboarding."""
        path = (
            f"{self._build_path(**kwargs)}/{identifier}"
            f"/legal_representatives/{legal_representative_id}/documents/{slot_key}"
        )
        return self._upload(path, {"file": self._build_file_payload(file)})

    @staticmethod
    def _build_file_payload(file):
        """
        Build the ``(filename, fileobj, content_type)`` tuple expected by httpx
        from either a path (``str`` / ``os.PathLike``) or a binary file-like
        object.
        """
        return build_file_payload(file)
