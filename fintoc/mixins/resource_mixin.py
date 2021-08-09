from abc import ABCMeta

from fintoc.helpers import get_resource_class, singularize


class ResourceMixin(metaclass=ABCMeta):
    mappings = {}

    def __init__(self, client, **kwargs):
        for key, value in kwargs.items():
            resource = singularize(self.__class__.mappings.get(key, key))
            if isinstance(value, list):
                klass = get_resource_class(resource, value=value)
                if klass is str:
                    setattr(self, key, [klass(x) for x in value])
                elif klass is dict:
                    setattr(self, key, [klass(x) for x in value])
                else:
                    setattr(self, key, [klass(client, **x) for x in value])
            elif isinstance(value, dict):
                klass = get_resource_class(resource, value=value)
                if klass is dict:
                    setattr(self, key, klass(**value))
                else:
                    setattr(self, key, klass(client, **value))
            else:
                setattr(self, key, value)
