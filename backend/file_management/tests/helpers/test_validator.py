import unittest

from file_management.helpers import validator

INVALID_EMAILS = ['test@example@example',
                  'test@example',
                  'testexample.com',
                  'testemail@test@gmail.com']

VALID_EMAILS = ['lhoang@codeustudents.com', 'lhoang@gmail.com', 'long.hb@teko.vn']


class EmailValidator(unittest.TestCase):
    def test_invalid_email(self):
        for invalid_email in INVALID_EMAILS:
            self.assertFalse(validator.validate_email(invalid_email))

    def test_valid_email(self):
        for valid_email in VALID_EMAILS:
            self.assertTrue(validator.validate_email(valid_email))


INVALID_FULLNAMES = ['Hoang Bao Long 123',
                     'Long   ',
                     'Hoang_Long']
VALID_FULLNAMES = ['Hoang Bao Long',
                   'Do Hoang Khanh',
                   'Mr Hoang']


class FullnameValidator(unittest.TestCase):
    def test_invalid_fullname(self):
        for invalid_fullname in INVALID_FULLNAMES:
            self.assertFalse(validator.validate_fullname(invalid_fullname))

    def test_valid_fullname(self):
        for valid_fullname in VALID_FULLNAMES:
            self.assertTrue(validator.validate_fullname(valid_fullname))


INVALID_PASSWORDS = ['AJCXSFx', 'hoang_1?????2']
VALID_PASSWORD = ['12345678', '12345678', 'lhoangbao']


class PasswordValidator(unittest.TestCase):
    def test_invalid_password(self):
        for invalid_password in INVALID_PASSWORDS:
            self.assertFalse(validator.validate_password(invalid_password))

    def test_valid_password(self):
        for valid_password in VALID_PASSWORD:
            self.assertTrue(validator.validate_password(valid_password))
