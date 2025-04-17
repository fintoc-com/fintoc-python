"""Module to hold the mixin for the managers."""

from abc import ABCMeta, abstractmethod

from fintoc.resource_handlers import (
    resource_create,
    resource_delete,
    resource_get,
    resource_list,
    resource_update,
)
from fintoc.utils import can_raise_fintoc_error, deprecate, get_resource_class


class ManagerMixin(metaclass=ABCMeta):  # pylint: disable=no-self-use

    """Represents the mixin for the managers."""

    def __init__(self, path, client):
        self._path = path
        self._client = client
        self._handlers = {
            "update": self.post_update_handler,
            "delete": self.post_delete_handler,
        }

    def __getattr__(self, attr):
        if attr not in self.__class__.methods:
            if attr == "all" and "list" in self.__class__.methods:
                return getattr(self, "_all")
            raise AttributeError(
                f"{self.__class__.__name__} has no attribute '{attr.lstrip('_')}'"
            )
        return getattr(self, f"_{attr}")

    @property
    @abstractmethod
    def resource(self):
        """
        This abstract property must be instanced as a class attribute
        when subclassing this mixin. It represents the name of the resource
        using snake_case.
        """

    @property
    @abstractmethod
    def methods(self):
        """
        This abstract property must be instanced as a class attribute
        when subclassing this mixin. It represents the methods that can
        be accessed using the manager. Must be an array with at least
        one of: ['all', 'get', 'create', 'update', 'delete'].
        """

    @can_raise_fintoc_error
    def _list(self, **kwargs):
        """
        List all instances of the resource being handled by the manager.
        :kwargs: can be used to filter the results, using the API parameters.
        """
        klass = get_resource_class(self.__class__.resource)
        objects = resource_list(
            client=self._client,
            path=self._build_path(**kwargs),
            klass=klass,
            handlers=self._handlers,
            methods=self.__class__.methods,
            params=kwargs,
        )
        return self.post_list_handler(objects, **kwargs)

    @deprecate(
        "all() is deprecated and will be removed in a future version. Use "
        "list() instead"
    )
    def _all(self, **kwargs):
        """
        Return all instances of the resource being handled by the manager.
        :kwargs: can be used to filter the results, using the API parameters.
        """
        return self._list(**kwargs)

    @can_raise_fintoc_error
    def _get(self, identifier, **kwargs):
        """
        Return an instance of the resource being handled by the manager,
        identified by :identifier:.
        """
        klass = get_resource_class(self.__class__.resource)
        object_ = resource_get(
            client=self._client,
            path=self._build_path(**kwargs),
            id_=identifier,
            klass=klass,
            handlers=self._handlers,
            methods=self.__class__.methods,
            params=kwargs,
        )
        return self.post_get_handler(object_, identifier, **kwargs)

    @can_raise_fintoc_error
    def _create(self, idempotency_key=None, path_=None, **kwargs):
        """
        Create an instance of the resource being handled by the manager.
        Data is passed using :kwargs:, as specified by the API.
        """
        klass = get_resource_class(self.__class__.resource)
        path = path_ if path_ else self._build_path(**kwargs)
        object_ = resource_create(
            client=self._client,
            path=path,
            klass=klass,
            handlers=self._handlers,
            methods=self.__class__.methods,
            params=kwargs,
            idempotency_key=idempotency_key,
        )
        return self.post_create_handler(object_, **kwargs)

    @can_raise_fintoc_error
    def _update(self, identifier, **kwargs):
        """
        Update an instance of the resource being handled by the manager,
        identified by :identifier:. Data is passed using :kwargs:, as
        specified by the API.
        """
        klass = get_resource_class(self.__class__.resource)
        object_ = resource_update(
            client=self._client,
            path=self._build_path(**kwargs),
            id_=identifier,
            klass=klass,
            handlers=self._handlers,
            methods=self.__class__.methods,
            params=kwargs,
        )
        return self.post_update_handler(object_, identifier, **kwargs)

    @can_raise_fintoc_error
    def _delete(self, identifier, **kwargs):
        """
        Delete an instance of the resource being handled by the manager,
        identified by :identifier:.
        """
        resource_delete(
            client=self._client,
            path=self._build_path(**kwargs),
            id_=identifier,
            params=kwargs,
        )
        return self.post_delete_handler(identifier, **kwargs)

    def _build_path(self, **kwargs):
        """
        Replaces placeholders in the path template with the corresponding
        values.
        """
        path = self._path
        for key, value in kwargs.items():
            path = path.replace("{" + key + "}", str(value))
        return path

    def post_list_handler(self, objects, **kwargs):
        """
        Hook that runs after the :list: method. Receives the objects fetched
        and **must** return them (either modified or as they came).
        """
        return objects

    def post_get_handler(self, object_, identifier, **kwargs):
        """
        Hook that runs after the :get: method. Receives the object fetched
        with its identifier and **must** return the object (either modified
        or as it came).
        """
        return object_

    def post_create_handler(self, object_, **kwargs):
        """
        Hook that runs after the :create: method. Receives the object fetched
        and **must** return the it (either modified or as it came).
        """
        return object_

    def post_update_handler(self, object_, identifier, **kwargs):
        """
        Hook that runs after the :update: method. Receives the object fetched
        with its identifier and **must** return the object (either modified
        or as it came).
        """
        return object_

    def post_delete_handler(self, identifier, **kwargs):
        """
        Hook that runs after the :create: method. Receives the identifier
        and **must** return it (either modified or as it came).
        """
        return identifier
