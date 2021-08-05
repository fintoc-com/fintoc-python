from importlib import import_module


def snake_to_pascal(snake_string):
    return "".join(word.title() for word in snake_string.split("_"))


def singularize(string):
    return string.rstrip("s")


def get_resource_class(snake_resource_name, value={}):
    if isinstance(value, dict):
        try:
            module = import_module(f"fintoc.resources.{snake_resource_name}")
            return getattr(module, snake_to_pascal(snake_resource_name), dict)
        except ModuleNotFoundError:
            return dict
    return str
