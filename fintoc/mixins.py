from abc import ABCMeta, abstractmethod
from importlib import import_module

import httpx

from fintoc.constants import API_BASE_URL, API_VERSION
from fintoc.helpers import get_resource_class, singularize, snake_to_pascal


class ResourceMixin(metaclass=ABCMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            resource = singularize(key)
            if isinstance(value, list):
                klass = get_resource_class(resource)
                setattr(self, key, [klass(**x) for x in value])
            elif isinstance(value, dict):
                klass = get_resource_class(key)
                setattr(self, key, klass(**value))
            else:
                setattr(self, key, value)


class ManagerMixin(metaclass=ABCMeta):
    def __init__(self, path, headers={}, params={}):
        self._path = path
        self._headers = headers
        self._params = params
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
                base_url=f"{API_BASE_URL}/{API_VERSION}", headers=self._headers
            )
        return self.__client

    def _all(self, **kwargs):
        lazy = kwargs.pop("lazy", True)
        response = self._client.get(self._path, params={**kwargs, **self._params})
        data = response.json()
        klass = get_resource_class(self.resource)
        return [klass(**x) for x in data]

    def _get(self, id_, **kwargs):
        response = self._client.get(
            f"{self._path}/{id_}", params={**kwargs, **self._params}
        )
        data = response.json()
        klass = get_resource_class(self.resource)
        return klass(**data)

    def _create(self, **kwargs):
        pass

    def _delete(self, id, **kwargs):
        pass
