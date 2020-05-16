import unittest

from bot.eft_ammo.accessor import Accessor


class AccessorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.accessor = Accessor(test_mode=True)

    def test_default_identifier(self):
        self.assertEqual('def', self.accessor.get_identifier('PS12'))

    def test_plus_identifier(self):
        self.assertEqual('+', self.accessor.get_identifier('+10'))

    def test_minus_identifier(self):
        self.assertEqual('-', self.accessor.get_identifier('-10'))

    def test_single_param_likeness_regex(self):
        self.assertEqual('(?=.*PS12)', self.accessor.get_regex('nom', ['PS12']))

    def test_multiple_param_likeness_regex(self):
        self.assertEqual('(?=.*PS12)(?=.*gzh)', self.accessor.get_regex('nom', ['PS12', 'gzh']))

    def test_single_param_exact_regex(self):
        self.assertEqual('^(10){1}$', self.accessor.get_regex('dmg', ['10']))

    def test_single_param_any_identifier_exact_regex(self):
        self.assertEqual('([+|-]10){1}$', self.accessor.get_regex('acc', ['10']))

    def test_single_param_plus_identifier_exact_regex(self):
        self.assertEqual('([+]10){1}$', self.accessor.get_regex('acc', ['+10']))

    def test_single_param_minus_identifier_exact_regex(self):
        self.assertEqual('([-]10){1}$', self.accessor.get_regex('acc', ['-10']))


if __name__ == '__main__':
    unittest.main()
