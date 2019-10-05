# coding=utf-8
import json
import logging
import time
from smtplib import SMTPException
from unittest.mock import patch

from file_management import repositories
from file_management.helpers import token
from file_management.helpers.faker import fake_user
from file_management.tests.api import APITestCase

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

valid_register = {
    "email": "lhoang@newtmail.com",
    "username": "lhoang",
    "fullname": "Hoang Bao Long",
    "password": "12345678"
}


@patch('file_management.services.my_mail')
class RegisterApiTestCase(APITestCase):
    def url(self):
        return '/api/register/'

    def method(self):
        return 'POST'

    def test_create_new_register(self, mork_mail):
        response = self.send_request(data=valid_register)
        mork_mail.send.assert_called_once()
        self.assertEqual(200, response.status_code)
        res_data = json.loads(response.data)['data']
        self.assertEqual(valid_register['username'], res_data['username'])
        self.assertEqual(valid_register['email'], res_data['email'])
        self.assertEqual(valid_register['fullname'], res_data['fullname'])

    def test_create_new_user_and_error_when_send_confrim_email(self, mork_mail):
        mork_mail.send.side_effect = SMTPException
        response = self.send_request(data=valid_register)
        mork_mail.send.assert_called_once()
        self.assertEqual(502, response.status_code)
        res_data = json.loads(response.data)
        custom_code = res_data['custom_code']
        self.assertEquals(custom_code, 'mail_server_err')

    def test_create_duplicate_user(self, mork_mail):
        self.send_request(data=valid_register)
        mork_mail.send.assert_called_once()
        response = self.send_request(data=valid_register)
        mork_mail.send.assert_called_once()
        self.assertEqual(409, response.status_code)
        res_data = json.loads(response.data)
        custom_code = res_data['custom_code']
        self.assertEquals(custom_code, 'registed_before')


CONFIRM_EMAIL_BASE_URL = '/api/register/confirm_email/'


class ConfrimEmailApiTestCase(APITestCase):
    def url(self):
        return CONFIRM_EMAIL_BASE_URL

    def method(self):
        return 'GET'

    def test_confirm_user_and_insert_to_user_table(self):
        fake_user.insert_some_register_to_db_for_testing()
        user_email = 'test01@coin-mail.com'
        confirm_token = token.encode_token(user_email, 1)
        response = self.send_request(url=CONFIRM_EMAIL_BASE_URL + confirm_token)
        self.assertEqual(200, response.status_code)
        user = repositories.user.find_one_by_email(user_email)
        self.assertNotEqual(user, None)
        self.assertEqual(user.email, user_email)

    def test_expired_token_when_confirm_email(self):
        fake_user.insert_some_register_to_db_for_testing()
        user_email = 'test01@coin-mail.com'
        confirm_token = token.encode_token(user_email, 0)
        time.sleep(1)
        response = self.send_request(url=CONFIRM_EMAIL_BASE_URL + confirm_token)
        self.assertEqual(401, response.status_code)
        res_data = json.loads(response.data)
        custom_code = res_data['custom_code']
        self.assertEquals(custom_code, 'invalid_token')
