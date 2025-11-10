import pytest

from fintoc.client import Client
from fintoc.mixins import ResourceMixin
from fintoc.resources import GenericFintocResource, Link


class EmptyMockResource(ResourceMixin):
    pass


class ComplexMockResource(ResourceMixin):
    mappings = {"resource": "link"}
    resource_identifier = "identifier"


class TestResourceMixinCreation:
    @pytest.fixture(autouse=True)
    def patch_http_client(self, patch_http_client):
        pass

    def setup_method(self):
        self.base_url = "https://test.com"
        self.api_key = "super_secret_api_key"
        self.api_version = None
        self.user_agent = "fintoc-python/test"
        self.params = {"first_param": "first_value", "second_param": "second_value"}
        self.client = Client(
            self.base_url,
            self.api_key,
            self.api_version,
            self.user_agent,
            params=self.params,
        )
        self.path = "/resources"
        self.handlers = {
            "update": lambda object_, identifier: print("Calling update...") or object_,
            "delete": lambda identifier: print("Calling delete...") or identifier,
        }

    def test_empty_mock_resource(self):
        methods = []
        data = {
            "id": "id0",
            "identifier": "identifier0",
            "resources": [
                {"id": "id1", "identifier": "identifier1"},
                {"id": "id2", "identifier": "identifier2"},
            ],
            "resource": {"id": "id3", "identifier": "identifier3"},
        }
        resource = EmptyMockResource(
            self.client, self.handlers, methods, self.path, **data
        )
        assert isinstance(resource, ResourceMixin)
        assert isinstance(resource.resource, GenericFintocResource)
        assert resource.resource.id == data["resource"]["id"]
        assert isinstance(resource.resources, list)
        for sub_resource in resource.resources:
            assert isinstance(sub_resource, GenericFintocResource)

    def test_complex_mock_resource(self):
        methods = []
        data = {
            "id": "id0",
            "identifier": "identifier0",
            "resources": [
                {"id": "id1", "identifier": "identifier1"},
                {"id": "id2", "identifier": "identifier2"},
            ],
            "resource": {"id": "id3", "identifier": "identifier3"},
        }
        resource = ComplexMockResource(
            self.client, self.handlers, methods, self.path, **data
        )
        assert isinstance(resource, ResourceMixin)
        assert isinstance(resource.resource, Link)
        assert resource.resource.id == data["resource"]["id"]
        assert isinstance(resource.resources, list)
        for sub_resource in resource.resources:
            assert isinstance(sub_resource, GenericFintocResource)

    def test_update_delete_methods_access(self):
        methods = ["delete"]
        data = {
            "id": "id0",
            "identifier": "identifier0",
            "resources": [
                {"id": "id1", "identifier": "identifier1"},
                {"id": "id2", "identifier": "identifier2"},
            ],
            "resource": {"id": "id3", "identifier": "identifier3"},
        }
        resource = EmptyMockResource(
            self.client, self.handlers, methods, self.path, **data
        )
        assert isinstance(resource, ResourceMixin)

        with pytest.raises(AttributeError):
            resource.update()

        resource.delete()


class TestMixinSerializeMethod:
    @pytest.fixture(autouse=True)
    def patch_http_client(self, patch_http_client):
        pass

    def setup_method(self):
        self.base_url = "https://test.com"
        self.api_key = "super_secret_api_key"
        self.api_version = None
        self.user_agent = "fintoc-python/test"
        self.params = {"first_param": "first_value", "second_param": "second_value"}
        self.client = Client(
            self.base_url,
            self.api_key,
            self.api_version,
            self.user_agent,
            params=self.params,
        )
        self.path = "/resources"
        self.handlers = {
            "update": lambda object_, identifier: print("Calling update...") or object_,
            "delete": lambda identifier: print("Calling delete...") or identifier,
        }

    def test_serialization_method(self):
        methods = ["delete"]
        data = {
            "id": "id0",
            "identifier": "identifier0",
            "resource": {"id": "id3", "identifier": "identifier3"},
        }
        resource = EmptyMockResource(
            self.client, self.handlers, methods, self.path, **data
        )
        assert resource.serialize() == data

    def test_array_serialization_method(self):
        methods = ["delete"]
        data = {
            "id": "id0",
            "identifier": "identifier0",
            "resources": [
                {"id": "id1", "identifier": "identifier1"},
                {"id": "id2", "identifier": "identifier2"},
            ],
            "resource": {"id": "id3", "identifier": "identifier3"},
        }
        resource = EmptyMockResource(
            self.client, self.handlers, methods, self.path, **data
        )
        assert resource.serialize() == data


class TestMixinUpdateAndDeleteMethods:
    @pytest.fixture(autouse=True)
    def patch_http_client(self, patch_http_client):
        pass

    def setup_method(self):
        self.base_url = "https://test.com"
        self.api_key = "super_secret_api_key"
        self.api_version = None
        self.user_agent = "fintoc-python/test"
        self.params = {"first_param": "first_value", "second_param": "second_value"}
        self.client = Client(
            self.base_url,
            self.api_key,
            self.api_version,
            self.user_agent,
            params=self.params,
        )
        self.path = "/resources"
        self.handlers = {
            "update": lambda object_, identifier: print("Calling update...") or object_,
            "delete": lambda identifier: print("Calling delete...") or identifier,
        }

    def test_complex_mock_resource_delete_method(self, capsys):
        methods = ["delete"]
        data = {
            "id": "id0",
            "identifier": "identifier0",
            "resources": [
                {"id": "id1", "identifier": "identifier1"},
                {"id": "id2", "identifier": "identifier2"},
            ],
            "resource": {"id": "id3", "identifier": "identifier3"},
        }
        resource = EmptyMockResource(
            self.client, self.handlers, methods, self.path, **data
        )
        identifier = resource.delete()

        captured = capsys.readouterr().out
        assert "delete" in captured

        assert identifier != data["identifier"]
        assert identifier == data["id"]

    def test_empty_mock_resource_delete_method(self, capsys):
        methods = ["delete"]
        data = {
            "id": "id0",
            "identifier": "identifier0",
            "resources": [
                {"id": "id1", "identifier": "identifier1"},
                {"id": "id2", "identifier": "identifier2"},
            ],
            "resource": {"id": "id3", "identifier": "identifier3"},
        }
        resource = ComplexMockResource(
            self.client, self.handlers, methods, self.path, **data
        )
        identifier = resource.delete()

        captured = capsys.readouterr().out
        assert "delete" in captured

        assert identifier != data["id"]
        assert identifier == data["identifier"]

    def test_complex_mock_resource_update_method(self, capsys):
        methods = ["update"]
        data = {
            "id": "id0",
            "identifier": "identifier0",
            "resources": [
                {"id": "id1", "identifier": "identifier1"},
                {"id": "id2", "identifier": "identifier2"},
            ],
            "resource": {"id": "id3", "identifier": "identifier3"},
        }
        resource = EmptyMockResource(
            self.client, self.handlers, methods, self.path, **data
        )

        resource.update()

        captured = capsys.readouterr().out
        assert "update" in captured

        assert data["identifier"] not in resource.url
        assert data["id"] in resource.url

    def test_empty_mock_resource_update_method(self, capsys):
        methods = ["update"]
        data = {
            "id": "id0",
            "identifier": "identifier0",
            "resources": [
                {"id": "id1", "identifier": "identifier1"},
                {"id": "id2", "identifier": "identifier2"},
            ],
            "resource": {"id": "id3", "identifier": "identifier3"},
        }
        resource = ComplexMockResource(
            self.client, self.handlers, methods, self.path, **data
        )
        resource.update()

        captured = capsys.readouterr().out
        assert "update" in captured

        assert data["id"] not in resource.url
        assert data["identifier"] in resource.url

    def test_resource_update_with_custom_path(self, capsys):
        methods = ["update"]
        data = {
            "id": "id0",
            "identifier": "identifier0",
        }
        resource = EmptyMockResource(
            self.client, self.handlers, methods, self.path, **data
        )

        custom_path = f"{self.path}/id0/cancel"
        resource.update(path_=custom_path)

        captured = capsys.readouterr().out
        assert "update" in captured
        assert resource.url == custom_path.lstrip("/")
