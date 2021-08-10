from fintoc.utils import singularize, snake_to_pascal


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

    def test_complex_plural_doesnt_work(self):
        complex_plural = "formulae"
        singular = singularize(complex_plural)
        assert singular != "formula"
