import datetime
from types import GeneratorType

import httpx
import pytest

from fintoc.constants import DATE_TIME_PATTERN
from fintoc.errors import ApiError, FintocError
from fintoc.resources import GenericFintocResource, Link
from fintoc.utils import (
    can_raise_fintoc_error,
    get_error_class,
    get_resource_class,
    is_iso_datetime,
    objetize,
    objetize_datetime,
    objetize_generator,
    serialize,
    singularize,
    snake_to_pascal,
)


class TestSnakeToPascal:
    def test_simple_string(self):
        snake = "this_is_a_test"
        pascal = snake_to_pascal(snake)
        assert pascal == "ThisIsATest"

    def test_complex_string(self):
        snake = "thIs_is_a_TEST"
        pascal = snake_to_pascal(snake)
        assert pascal == "ThisIsATest"

    def test_pascale_cased_string(self):
        initial = "ThisIsATest"
        pascal = snake_to_pascal(initial)
        assert pascal == "Thisisatest"


class TestSingularize:
    def test_plural_string(self):
        string = "movements"
        singular = singularize(string)
        assert singular == "movement"

    def test_singular_string(self):
        string = "movement"
        singular = singularize(string)
        assert singular == "movement"

    def test_complex_plural_does_not_work(self):
        complex_plural = "formulae"
        singular = singularize(complex_plural)
        assert singular != "formula"


class TestIsISODateTime:
    def test_valid_iso_format(self):
        valid_iso_datetime_string = "2021-08-13T13:40:40Z"
        assert is_iso_datetime(valid_iso_datetime_string)

    def test_valid_iso_miliseconds_format(self):  # TEMPORARY
        valid_iso_miliseconds_datetime_string = "2021-08-13T13:40:40.811Z"
        assert is_iso_datetime(valid_iso_miliseconds_datetime_string)

    def test_invalid_iso_string_format(self):
        invalid_iso_datetime_string = "This is not a date"
        assert not is_iso_datetime(invalid_iso_datetime_string)

    def test_invalid_iso_number_format(self):
        invalid_iso_datetime_string = "1105122"
        assert not is_iso_datetime(invalid_iso_datetime_string)


class TestGetResourceClass:
    def test_default_valid_resource(self):
        resource = "link"
        klass = get_resource_class(resource)
        assert klass is Link

    def test_default_invalid_resource(self):
        resource = "this_resource_does_not_exist"
        klass = get_resource_class(resource)
        assert klass is GenericFintocResource

    def test_iso_datetime_resource(self):
        resource = "any_resource"
        klass = get_resource_class(resource, value="2021-08-13T13:40:40.811Z")
        assert klass is objetize_datetime

    def test_string_resource(self):
        resource = "any_resource"
        klass = get_resource_class(resource, value="test-value")
        assert klass is str

    def test_int_resource(self):
        resource = "any_resource"
        klass = get_resource_class(resource, value=15)
        assert klass is int

    def test_bool_resource(self):
        resource = "any_resource"
        klass = get_resource_class(resource, value=True)
        assert klass is bool


class TestGetErrorClass:
    def test_valid_error(self):
        error_name = "api_error"
        error = get_error_class(error_name)
        assert error is ApiError

    def test_invalid_error(self):
        error_name = "this_error_does_not_exist"
        error = get_error_class(error_name)
        assert error is FintocError


class TestCanRaiseFintocError:
    @pytest.fixture(autouse=True)
    def patch_http_error(self, patch_http_error):
        pass

    def setup_method(self):
        def no_error():
            pass

        def raise_http_status_error():
            raise httpx.HTTPStatusError(
                message="HTTP Status Error",
                response=httpx.Response(
                    status_code=400, json={"error": {"type": "api_error"}}
                ),
                request=httpx.Request("GET", "/"),
            )

        def raise_connect_error():
            raise httpx.ConnectError(message="Connection Error")

        def raise_generic_error():
            raise ValueError("Not HTTP Error")

        self.no_error = no_error
        self.raise_http_status_error = raise_http_status_error
        self.raise_connect_error = raise_connect_error
        self.raise_generic_error = raise_generic_error

    def test_no_error(self):
        wrapped = can_raise_fintoc_error(self.no_error)
        wrapped()

    def test_http_status_error(self):
        wrapped = can_raise_fintoc_error(self.raise_http_status_error)
        with pytest.raises(Exception) as execinfo:
            wrapped()
        assert isinstance(execinfo.value, FintocError)

    def test_connect_error(self):
        wrapped = can_raise_fintoc_error(self.raise_connect_error)
        with pytest.raises(Exception) as execinfo:
            wrapped()
        assert not isinstance(execinfo.value, FintocError)

    def test_generic_error(self):
        wrapped = can_raise_fintoc_error(self.raise_generic_error)
        with pytest.raises(Exception) as execinfo:
            wrapped()
        assert not isinstance(execinfo.value, FintocError)


# Example class for the objetize tests
class ExampleClass:
    def __init__(self, client, handlers, methods, path, **kwargs):
        self.client = client
        self.handlers = handlers
        self.methods = methods
        self.path = path
        self.data = kwargs

    def serialize(self):
        return self.data


class TestSerialize:
    def test_string_serialization(self):
        string = "This is a string"
        assert serialize(string) == string

    def test_boolean_serialization(self):
        boolean = True
        assert serialize(boolean) == boolean

    def test_int_serialization(self):
        integer = 3
        assert serialize(integer) == integer

    def test_none_serialization(self):
        none = None
        assert serialize(none) == none

    def test_datetime_serialization(self):
        now = datetime.datetime.now()
        assert isinstance(now, datetime.datetime)
        assert isinstance(serialize(now), str)
        assert serialize(now) == now.strftime(DATE_TIME_PATTERN)

    def test_object_with_serialize_method_serialization(self):
        data = {"a": "b", "c": "d"}
        object_ = ExampleClass("client", ["handler"], ["method"], "path", **data)
        assert serialize(object_) == object_.serialize()


class TestObjetize:
    def setup_method(self):
        self.client = "This is a client"
        self.data = {
            "id": "obj_3nlaf830FBbfF83",
            "name": "Sample Name",
            "number": 47,
        }

    def test_string_objetization(self):
        data = "This is data"
        object_ = objetize(str, self.client, data)
        assert isinstance(object_, str)
        assert object_ == data

    def test_dictionary_objetization(self):
        object_ = objetize(dict, self.client, self.data)
        assert isinstance(object_, dict)
        assert object_ == self.data

    def test_complete_objetization(self):
        object_ = objetize(ExampleClass, self.client, self.data)
        assert isinstance(object_, ExampleClass)
        assert object_.data["id"] == self.data["id"]


class TestObjetizeDateTime:
    def setup_method(self):
        self.valid_string = "2021-12-16T12:24:44Z"
        self.valid_miliseconds_string = "2021-12-16T12:24:44.397Z"
        self.obviously_invalid_string = "This is not a date"
        self.deceptively_invalid_string = "1105122"

    def test_valid_string(self):
        parsed = objetize_datetime(self.valid_string)
        assert isinstance(parsed, datetime.datetime)

    def test_valid_miliseconds_string(self):  # TEMPORARY
        parsed = objetize_datetime(self.valid_miliseconds_string)
        assert isinstance(parsed, datetime.datetime)

    def test_obviously_invalid_string(self):
        with pytest.raises(ValueError):
            objetize_datetime(self.obviously_invalid_string)

    def test_deceptively_invalid_string(self):
        with pytest.raises(ValueError):
            objetize_datetime(self.deceptively_invalid_string)


class TestObjetizeGenerator:
    def setup_method(self):
        self.client = "This is a client"

        def get_generator():
            for iii in range(10):
                yield {
                    "id": "obj_3nlaf830FBbfF83",
                    "name": "Sample Name",
                    "number": iii,
                }

        self.get_generator = get_generator

    def test_generator_objetization(self):
        generator = self.get_generator()
        assert isinstance(generator, GeneratorType)

        objetized_generator = objetize_generator(generator, ExampleClass, self.client)
        assert isinstance(objetized_generator, GeneratorType)

        for object_ in objetized_generator:
            assert isinstance(object_, ExampleClass)
