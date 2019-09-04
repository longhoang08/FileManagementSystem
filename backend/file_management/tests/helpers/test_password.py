import unittest

from file_management.helpers import password
from file_management.helpers import validator


class TestPassword(unittest.TestCase):
    def test_verify_password_after_using_hash_passowrd_function(self):
        original_password = 'itismypassword'
        password_hash = password.hash_password(original_password)
        self.assertTrue(password.verify_password(password_hash, original_password))

    def test_random_password_generator(self):
        for i in range(100):
            random_password = password.gen_new_password()
            self.assertTrue(validator.validate_password(random_password))
