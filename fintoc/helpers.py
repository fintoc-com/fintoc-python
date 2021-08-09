from importlib import import_module

import httpx

from fintoc.errors import FintocError


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


def get_error_class(snake_error_name):
    module = import_module("fintoc.errors")
    return getattr(module, snake_to_pascal(snake_error_name), FintocError)


def can_raise_http_error(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except httpx.HTTPError as exc:
            error_data = exc.response.json()
            error = get_error_class(error_data["error"]["type"])
            raise error(error_data["error"]) from None

    return wrapper
