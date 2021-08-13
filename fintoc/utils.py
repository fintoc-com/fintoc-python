"""Module to hold every generalized utility on the SDK."""

import datetime
from importlib import import_module

import httpx
from dateutil import parser

from fintoc.errors import FintocError


def snake_to_pascal(snake_string):
    """Return the snake-cased string as pascal case."""
    return "".join(word.title() for word in snake_string.split("_"))


def singularize(string):
    """Remove the last 's' from a string if exists."""
    return string.rstrip("s")


def is_iso_datetime(string):
    """
    Try to parse a string as an ISO date. If it succeeds, return True.
    Otherwise, return False.
    """
    try:
        parser.isoparse(string)
        return True
    except ValueError:
        return False


def get_resource_class(snake_resource_name, value={}):
    """
    Get the class that corresponds to a resource using its
    name (in snake case) and its value.
    """
    if isinstance(value, dict):
        module = import_module("fintoc.resources")
        try:
            return getattr(module, snake_to_pascal(snake_resource_name))
        except AttributeError:
            return getattr(module, "GenericFintocResource")
    if isinstance(value, str) and is_iso_datetime(value):
        return parser.isoparse
    return type(value)


def get_error_class(snake_error_name):
    """
    Given an error name (in snake case), return the appropriate
    error class.
    """
    module = import_module("fintoc.errors")
    return getattr(module, snake_to_pascal(snake_error_name), FintocError)


def can_raise_http_error(function):
    """
    Decorator that catches HTTPError exceptions and raises custom
    Fintoc errors instead.
    """

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except httpx.HTTPError as exc:
            error_data = exc.response.json()
            error = get_error_class(error_data["error"]["type"])
            raise error(error_data["error"]) from None

    return wrapper


def serialize(object_):
    """Serializes an object."""
    if callable(getattr(object_, "serialize", None)):
        return object_.serialize()
    if isinstance(object_, datetime.datetime):
        return object_.isoformat()
    return object_


def objetize(klass, client, data, handlers={}, methods=[], path=None):
    """Transform the :data: object into an object with class :klass:."""
    if data is None:
        return None
    if klass in [str, int, dict, bool, parser.isoparse]:
        return klass(data)
    return klass(client, handlers, methods, path, **data)


def objetize_generator(generator, klass, client, handlers={}, methods=[], path=None):
    """
    Transform a generator of dictionaries into a generator of
    objects with class :klass:.
    """
    for element in generator:
        yield objetize(klass, client, element, handlers, methods, path)
