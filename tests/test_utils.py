import unittest
from fintoc import utils


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.dict_ = {"spam": 42, "ham": "spam", "bacon": {"spam": -1}}

    def test_pick(self):
        self.assertEqual(utils.pick(self.dict_, "ham"), {"ham": "spam"})
        self.assertEqual(utils.pick(self.dict_, "eggs"), {})

    def test_rename_keys(self):
        self.assertEqual(
            utils.rename_keys(self.dict_, ("spam", "eggs")),
            {"eggs": 42, "ham": "spam", "bacon": {"eggs": -1}},
        )

    def test_snake_to_pascal(self):
        self.assertEqual(
            utils.snake_to_pascal("this_example_should_be_good_enough"),
            "ThisExampleShouldBeGoodEnough",
        )
        self.assertEqual(
            utils.snake_to_pascal("internal_server_error_error"),
            "InternalServerErrorError",
        )


if __name__ == "__main__":
    unittest.main()
