import unittest

import config
from lib.rsa import RSA

class TestRSA(unittest.TestCase):
    def test_rsa2_sign_and_verify(self):
        rsa = RSA(config.private_key_path, "RSA2")
        message = "123"
        signature = rsa.sign(message)

        rsa = RSA(config.public_key_path, "RSA2")
        verification = rsa.verify(message, signature)
        self.assertTrue(verification)

    def test_rsa_sign_and_verify(self):
        rsa = RSA(config.private_key_path, "RSA")
        message = "123"
        signature = rsa.sign(message)

        rsa = RSA(config.public_key_path, "RSA")
        verification = rsa.verify(message, signature)
        self.assertTrue(verification)