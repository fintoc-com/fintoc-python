from abc import ABCMeta, abstractmethod

import httpx

from fintoc.helpers import get_resource_class


class ManagerMixin(metaclass=ABCMeta):
    def __init__(self, path, client_data):
        self._path = path
        self._client_data = client_data
        self.__client = None

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

    @property
    def _client(self):
        if not self.__client:
            self.__client = httpx.Client(
                base_url=self._client_data.base_url,
                headers=self._client_data.headers,
                params=self._client_data.params,
            )
        return self.__client

    def _all(self, **kwargs):
        lazy = kwargs.pop("lazy", True)
        response = self._client.get(self._path, params=kwargs)
        data = response.json()
        klass = get_resource_class(self.resource)
        return [klass(self._client_data, **x) for x in data]

    def _get(self, id_, **kwargs):
        response = self._client.get(f"{self._path}/{id_}", params=kwargs)
        data = response.json()
        klass = get_resource_class(self.resource)
        object_ = klass(self._client_data, **data)
        return self._post_get_handler(object_, id_, **kwargs)

    def _create(self, **kwargs):
        response = self._client.post(
            self._path, json=kwargs
        )
        data = response.json()
        klass = get_resource_class(self.resource)
        object_ = klass(self._client_data, **data)
        return self._post_create_handler(object_, **kwargs)

    def _delete(self, id_, **kwargs):
        response = self._client.delete(f"{self._path}/{id_}", params=kwargs)
        return self._post_delete_handler(id_, **kwargs)

    def _post_all_handler(self, objects_, **kwargs):
        return objects_

    def _post_get_handler(self, object_, id_, **kwargs):
        return object_

    def _post_create_handler(self, object_, **kwargs):
        return object_

    def _post_delete_handler(self, id_, **kwargs):
        return id_
