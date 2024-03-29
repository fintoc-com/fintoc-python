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
