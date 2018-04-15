import unittest

from bot.handlers.verifiers import Verifier


class TestEVAVerifier(unittest.TestCase):

    def test_is_a_number(self):
        good_cpf = "12345678901"
        bad_cpf = "123456780oi1"
        self.assertTrue(Verifier.only_numbers(good_cpf))
        self.assertFalse(Verifier.only_numbers(bad_cpf))
