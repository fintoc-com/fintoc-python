from fintoc.client import Client
from fintoc.core import Fintoc
from fintoc.mixins import ManagerMixin


class TestCoreFintocObject:
    def test_object_creations(self):
        # pylint: disable=protected-access
        api_key = "super_secret_api_key"
        fintoc = Fintoc(api_key)
        assert isinstance(fintoc._client, Client)
        assert isinstance(fintoc.links, ManagerMixin)
        assert isinstance(fintoc.webhook_endpoints, ManagerMixin)

    def test_fintoc_creation_with_api_version(self):
        # pylint: disable=protected-access
        api_key = "super_secret_api_key"
        api_version = "2023-01-01"
        fintoc = Fintoc(api_key, api_version)
        assert fintoc._client.headers["Fintoc-Version"] == api_version

    def test_fintoc_creation_without_api_version(self):
        # pylint: disable=protected-access
        api_key = "super_secret_api_key"
        fintoc = Fintoc(api_key)
        assert "Fintoc-Version" not in fintoc._client.headers
