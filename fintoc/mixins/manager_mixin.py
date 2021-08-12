"""Module to hold the mixin for the managers."""

from abc import ABCMeta, abstractmethod

from fintoc.resource_handlers import resource_all, resource_create, resource_get
from fintoc.utils import can_raise_http_error, get_resource_class


class ManagerMixin(metaclass=ABCMeta):  # pylint: disable=no-self-use

    """Represents the mixin for the managers."""

    def __init__(self, path, client):
        self._path = path
        self._client = client.extend()
        self._handlers = {
            "update": self.post_update_handler,
            "delete": self.post_delete_handler,
        }

    def __getattr__(self, attr):
        if attr not in self.__class__.methods:
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

    @can_raise_http_error
    def _all(self, **kwargs):
        """
        Return all instances of the resource being handled by the manager.
        :kwargs: can be used to filter the results, using the API parameters.
        """
        klass = get_resource_class(self.__class__.resource)
        objects = resource_all(
            client=self._client,
            path=self._path,
            klass=klass,
            handlers=self._handlers,
            methods=self.__class__.methods,
            params=kwargs,
        )
        return self.post_all_handler(objects, **kwargs)

    @can_raise_http_error
    def _get(self, identifier, **kwargs):
        """
        Return an instance of the resource being handled by the manager,
        identified by :identifier:.
        """
        klass = get_resource_class(self.__class__.resource)
        object_ = resource_get(
            client=self._client,
            path=self._path,
            id_=identifier,
            klass=klass,
            handlers=self._handlers,
            methods=self.__class__.methods,
            params=kwargs,
        )
        return self.post_get_handler(object_, identifier, **kwargs)

    @can_raise_http_error
    def _create(self, **kwargs):
        """
        Create an instance of the resource being handled by the manager.
        Data is passed using :kwargs:, as specified by the API.
        """
        klass = get_resource_class(self.__class__.resource)
        object_ = resource_create(
            client=self._client,
            path=self._path,
            klass=klass,
            handlers=self._handlers,
            methods=self.__class__.methods,
            params=kwargs,
        )
        return self.post_create_handler(object_, **kwargs)

    @can_raise_http_error
    def _update(self, identifier, **kwargs):
        """
        Update an instance of the resource being handled by the manager,
        identified by :identifier:. Data is passed using :kwargs:, as
        specified by the API.
        """
        object_ = self._get(identifier)
        return object_.update(**kwargs)

    @can_raise_http_error
    def _delete(self, identifier, **kwargs):
        """
        Delete an instance of the resource being handled by the manager,
        identified by :identifier:.
        """
        object_ = self._get(identifier)
        return object_.delete(**kwargs)

    def post_all_handler(self, objects, **kwargs):
        """
        Hook that runs after the :all: method. Receives the objects fetched
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
