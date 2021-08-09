from abc import ABCMeta, abstractmethod

from fintoc.utils import can_raise_http_error, get_resource_class
from fintoc.resource_handlers import resource_all, resource_create, resource_get


class ManagerMixin(metaclass=ABCMeta):
    def __init__(self, path, client):
        self._path = path
        self._client = client.extend()
        self._handlers = {
            "update": self.post_update_handler,
            "delete": self.post_delete_handler,
        }

    def __getattr__(self, attr):
        if attr not in self.methods:
            raise AttributeError(
                f"{self.__class__.__name__} has no attribute '{attr.lstrip('_')}'"
            )
        return getattr(self, f"_{attr}")

    @property
    @abstractmethod
    def resource(self):
        pass

    @property
    @abstractmethod
    def methods(self):
        pass

    @can_raise_http_error
    def _all(self, **kwargs):
        klass = get_resource_class(self.resource)
        objects = resource_all(
            client=self._client,
            path=self._path,
            klass=klass,
            handlers=self._handlers,
            methods=self.methods,
            params=kwargs,
        )
        return self.post_all_handler(objects, **kwargs)

    @can_raise_http_error
    def _get(self, identifier, **kwargs):
        klass = get_resource_class(self.resource)
        object_ = resource_get(
            client=self._client,
            path=self._path,
            id_=identifier,
            klass=klass,
            handlers=self._handlers,
            methods=self.methods,
            params=kwargs,
        )
        return self.post_get_handler(object_, identifier, **kwargs)

    @can_raise_http_error
    def _create(self, **kwargs):
        klass = get_resource_class(self.resource)
        object_ = resource_create(
            client=self._client,
            path=self._path,
            klass=klass,
            handlers=self._handlers,
            methods=self.methods,
            params=kwargs,
        )
        return self.post_create_handler(object_, **kwargs)

    @can_raise_http_error
    def _update(self, identifier, **kwargs):
        object_ = self._get(identifier)
        return object_.update(**kwargs)

    @can_raise_http_error
    def _delete(self, identifier, **kwargs):
        object_ = self._get(identifier)
        return object_.delete(**kwargs)

    def post_all_handler(self, objects, **kwargs):
        return objects

    def post_get_handler(self, object_, identifier, **kwargs):
        return object_

    def post_create_handler(self, object_, **kwargs):
        return object_

    def post_update_handler(self, object_, identifier, **kwargs):
        return object_

    def post_delete_handler(self, identifier, **kwargs):
        return identifier
