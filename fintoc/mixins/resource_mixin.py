"""Module to hold the mixin for the resources."""

from abc import ABCMeta

from fintoc.resource_handlers import resource_delete, resource_update
from fintoc.utils import (
    can_raise_http_error,
    get_resource_class,
    objetize,
    serialize,
    singularize,
)


class ResourceMixin(metaclass=ABCMeta):

    """Represents the mixin for the resources."""

    mappings = {}
    resource_identifier = "id"

    def __init__(self, client, handlers, methods, path, **kwargs):
        self._client = client
        self._handlers = handlers
        self._methods = methods
        self._path = path
        self._attributes = []

        for key, value in kwargs.items():
            try:
                resource = self.__class__.mappings.get(key, key)
                if isinstance(value, list):
                    resource = singularize(resource)
                    element = {} if not value else value[0]
                    klass = get_resource_class(resource, value=element)
                    setattr(self, key, [objetize(klass, client, x) for x in value])
                else:
                    klass = get_resource_class(resource, value=value)
                    setattr(self, key, objetize(klass, client, value))
                self._attributes.append(key)
            except NameError:  # pragma: no cover
                pass

    def __getattr__(self, attr):
        if attr not in self._methods:
            raise AttributeError(
                f"{self.__class__.__name__} has no attribute '{attr.lstrip('_')}'"
            )
        return getattr(self, f"_{attr}")

    def serialize(self):
        """Serialize the resource."""
        serialized = {}
        for key in self._attributes:
            element = (
                [serialize(x) for x in self.__dict__[key]]
                if isinstance(self.__dict__[key], list)
                else serialize(self.__dict__[key])
            )
            serialized = {**serialized, key: element}
        return serialized

    @can_raise_http_error
    def _update(self, **kwargs):
        id_ = getattr(self, self.__class__.resource_identifier)
        object_ = resource_update(
            client=self._client,
            path=self._path,
            id_=id_,
            klass=self.__class__,
            handlers=self._handlers,
            methods=self._methods,
            params=kwargs,
        )
        object_ = self._handlers.get("update")(object_, id_, **kwargs)
        self.__dict__.update(object_.__dict__)
        return self

    @can_raise_http_error
    def _delete(self, **kwargs):
        identifier = getattr(self, self.__class__.resource_identifier)
        resource_delete(
            client=self._client,
            path=self._path,
            id_=self.id,
            params=kwargs,
        )
        return self._handlers.get("delete")(identifier, **kwargs)
