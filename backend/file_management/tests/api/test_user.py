# coding=utf-8
import json
import logging
import re
from unittest.mock import patch

from file_management.helpers.faker import fake_user
from file_management.tests.api import APITestCase

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

WRONG_LOGIN_REQUEST = {
    'username': fake_user.VALID_USERS[0]['username'],
    'password': '123456789'
}

VALID_LOGIN_REQUEST = {
    'username': fake_user.VALID_USERS[0]['username'],
    'password': fake_user.VALID_USERS[0]['password']
}


class LoginApiTestCase(APITestCase):
    def url(self):
        return '/api/users/login'

    def method(self):
        return 'POST'

    def test_login_wrong_account(self):
        fake_user.insert_some_user_to_db_for_testing()
        response = self.send_request(WRONG_LOGIN_REQUEST)
        self.assertEqual(401, response.status_code)
        res_data = json.loads(response.data)
        custom_code = res_data['custom_code']
        self.assertEquals(custom_code, 'wrong_pass')

    def test_cookies_when_login_success(self):
        fake_user.insert_some_user_to_db_for_testing()
        response = self.send_request(VALID_LOGIN_REQUEST)
        self.assertEqual(200, response.status_code)
        cookies = response.headers.getlist('Set-Cookie')
        for cookie in cookies:
            token_regex = r'.*access_token_cookie.*'
            pattern = re.compile(token_regex)
            if (pattern.match(str(cookie))):
                assert True
                return
        # Cookie not found
        assert False


class LogoutApiTestCase(APITestCase):
    def url(self):
        return '/api/users/logout'

    def method(self):
        return 'POST'

    @patch('boilerplate.api.logout.unset_jwt_cookies')
    def test_delete_cookies_when_logout(self, mock_jwt):
        fake_user.insert_some_user_to_db_for_testing()
        response = self.send_request(url='/api/login/', data=VALID_LOGIN_REQUEST)
        self.assertEqual(200, response.status_code)
        response = self.send_request(url='/api/logout/')
        self.assertEqual(200, response.status_code)
        mock_jwt.assert_called_once()
