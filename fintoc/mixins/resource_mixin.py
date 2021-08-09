from abc import ABCMeta

from fintoc.helpers import (
    can_raise_http_error,
    get_resource_class,
    objetize,
    singularize,
)


class ResourceMixin(metaclass=ABCMeta):
    mappings = {}

    def __init__(self, client, handlers, methods, path, **kwargs):
        self._client = client
        self._handlers = handlers
        self._methods = methods
        self._path = path

        for key, value in kwargs.items():
            resource = singularize(self.__class__.mappings.get(key, key))
            if isinstance(value, list):
                klass = get_resource_class(resource, value=value)
                setattr(self, key, [objetize(klass, client, x) for x in value])
            elif isinstance(value, dict):
                klass = get_resource_class(resource, value=value)
                setattr(self, key, objetize(klass, client, value))
            else:
                setattr(self, key, value)

    def __getattr__(self, attr):
        if attr in ["update", "delete"]:
            if attr not in self._methods:
                raise AttributeError(
                    f"{self.__class__.__name__} has no attribute '{attr.lstrip('_')}'"
                )
            return getattr(self, f"_{attr}")
        return self.__dict__[attr]

    @can_raise_http_error
    def _update(self, **kwargs):
        response = self._client.request(
            f"{self._path}/{self.id}", method="patch", json=kwargs
        )
        data = response.json()
        object_ = objetize(
            self.__class__,
            self._client,
            data,
            self._handlers,
            self._methods,
            self._path,
        )
        object_ = self._handlers.get("update")(object_, object_.id, **kwargs)
        self.__dict__.update(object_.__dict__)

    @can_raise_http_error
    def _delete(self, **kwargs):
        self._client.request(f"{self._path}/{self.id}", method="delete", params=kwargs)
        return self._handlers.get("update")(self.id, **kwargs)
