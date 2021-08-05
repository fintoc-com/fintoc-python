from abc import ABCMeta

from fintoc.helpers import get_resource_class, singularize


class ResourceMixin(metaclass=ABCMeta):
    def __init__(self, client_data, **kwargs):
        for key, value in kwargs.items():
            resource = singularize(key)
            if isinstance(value, list):
                klass = get_resource_class(resource, value=value)
                if klass is str:
                    setattr(self, key, [klass(x) for x in value])
                elif klass is dict:
                    setattr(self, key, [klass(x) for x in value])
                else:
                    setattr(self, key, [klass(client_data, **x) for x in value])
            elif isinstance(value, dict):
                klass = get_resource_class(key, value=value)
                if klass is dict:
                    setattr(self, key, klass(**value))
                else:
                    setattr(self, key, klass(client_data, **value))
            else:
                setattr(self, key, value)
