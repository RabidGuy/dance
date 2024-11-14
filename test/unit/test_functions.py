import unittest

import dance


class test_get_actors_from_tokens(unittest.TestCase):
    def test_correct_number_of_colons_passes(self):
        try:
            row = [{"text": "George: 10", "filepath": "", "linenumber": 1}]
            dance.get_actors_from_tokens(row)
        except TypeError:
            self.fail("get_actors_from_tokens raised TypeError")
        except SyntaxError:
            self.fail("get_actors_from_tokens raised SyntaxError")

    def test_missing_colon_raises_value_error(self):
        with self.assertRaises(SyntaxError):
            row = [{"text": "George 10", "filepath": "", "linenumber": 1}]
            dance.get_actors_from_tokens(row)

    def test_too_many_colons_raises_value_error(self):
        with self.assertRaises(SyntaxError):
            row = [{"text": "George:: 10", "filepath": "", "linenumber": 1}]
            dance.get_actors_from_tokens(row)
