from abc import ABCMeta, abstractmethod

from fintoc.helpers import (
    can_raise_http_error,
    get_resource_class,
    objetize,
    objetize_generator,
)


class ManagerMixin(metaclass=ABCMeta):
    def __init__(self, path, client):
        self._path = path
        self._client = client
        self._handlers = {
            "update": self._post_update_handler,
            "delete": self._post_delete_handler,
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
        lazy = kwargs.pop("lazy", True)
        data = self._client.request(self._path, paginated=True, params=kwargs)
        klass = get_resource_class(self.resource)
        if lazy:
            return objetize_generator(
                data,
                klass,
                self._client,
                handlers=self._handlers,
                methods=self.methods,
                path=self._path,
            )
        return [
            objetize(
                klass,
                self._client,
                data,
                handlers=self._handlers,
                methods=self.methods,
                path=self._path,
            )
            for x in data
        ]

    @can_raise_http_error
    def _get(self, id_, **kwargs):
        response = self._client.request(
            f"{self._path}/{id_}", method="get", params=kwargs
        )
        data = response.json()
        klass = get_resource_class(self.resource)
        object_ = objetize(
            klass,
            self._client,
            data,
            handlers=self._handlers,
            methods=self.methods,
            path=self._path,
        )
        return self._post_get_handler(object_, id_, **kwargs)

    @can_raise_http_error
    def _create(self, **kwargs):
        response = self._client.request(self._path, method="post", json=kwargs)
        data = response.json()
        klass = get_resource_class(self.resource)
        object_ = objetize(
            klass,
            self._client,
            data,
            handlers=self._handlers,
            methods=self.methods,
            path=self._path,
        )
        return self._post_create_handler(object_, **kwargs)

    @can_raise_http_error
    def _update(self, id_, **kwargs):
        object_ = self._get(id_)
        return object_.update(**kwargs)

    @can_raise_http_error
    def _delete(self, id_, **kwargs):
        object_ = self._get(id_)
        return object_.delete(**kwargs)

    def _post_all_handler(self, objects_, **kwargs):
        return objects_

    def _post_get_handler(self, object_, id_, **kwargs):
        return object_

    def _post_create_handler(self, object_, **kwargs):
        return object_

    def _post_update_handler(self, object_, id_, **kwargs):
        return object_

    def _post_delete_handler(self, id_, **kwargs):
        return id_
