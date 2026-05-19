"""Module to hold the disputes manager."""

from fintoc.managers.dispute_documents_manager import DisputeDocumentsManager
from fintoc.mixins import ManagerMixin


# pylint: disable=duplicate-code
class DisputesManager(ManagerMixin):

    """Represents a disputes manager."""

    resource = "dispute"
    methods = ["list", "get", "submit_for_review"]

    def __init__(self, path, client):
        super().__init__(path, client)
        self.__documents_manager = None

    def _submit_for_review(self, identifier, **kwargs):
        """Submit a dispute for review."""
        path = f"{self._build_path(**kwargs)}/{identifier}/submit_for_review"
        return self._create(path_=path, **kwargs)

    @property
    def documents(self):
        """Proxies the dispute documents manager."""
        if self.__documents_manager is None:
            self.__documents_manager = DisputeDocumentsManager(
                "/v1/disputes/{dispute_id}/documents",
                self._client,
            )
        return self.__documents_manager

    @documents.setter
    def documents(self, new_value):  # pylint: disable=no-self-use
        raise NameError("Attribute name corresponds to a manager")
