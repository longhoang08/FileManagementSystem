# coding=utf-8
import json
import logging
from unittest.mock import patch

from file_management import services
from file_management.extensions.custom_exception import WrongPasswordException
from file_management.helpers.faker import fake_user
from file_management.tests.api import APITestCase

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)

VALID_CHANGE_PASSWORD_REQUEST = {
    'email': fake_user.VALID_USERS[0]['email'],
    'current_password': fake_user.VALID_USERS[0]['password'],
    'new_password': 'newpassword1'
}


@patch('file_management.api.profile.services.token.check_jwt_token')
class ChangePasswordApiTestCase(APITestCase):
    def url(self):
        return '/api/profile/change_password'

    def method(self):
        return 'POST'

    def test_change_password_with_valid_token_and_check_new_password(self, mock_jwt):
        fake_user.insert_some_user_to_db_for_testing()
        mock_jwt.return_value = VALID_CHANGE_PASSWORD_REQUEST['email']
        response = self.send_request(data=VALID_CHANGE_PASSWORD_REQUEST)
        mock_jwt.assert_called_once()
        self.assertEquals(200, response.status_code)

        try:
            services.user.check_username_and_password(
                username=fake_user.VALID_USERS[0]['username'],
                password=VALID_CHANGE_PASSWORD_REQUEST['new_password'],
            )
        except:
            assert False

        with self.assertRaises(WrongPasswordException):
            services.user.check_username_and_password(
                username=fake_user.VALID_USERS[0]['username'],
                password=VALID_CHANGE_PASSWORD_REQUEST['current_password'],
            )

    def test_change_password_equal_to_last_five_password(self, mock_jwt):
        fake_user.insert_some_user_to_db_for_testing()
        mock_jwt.return_value = VALID_CHANGE_PASSWORD_REQUEST['email']
        response = self.send_request(data={
            'email': fake_user.VALID_USERS[0]['email'],
            'current_password': fake_user.VALID_USERS[0]['password'],
            'new_password': 'newpassword1'
        })
        self.assertEquals(200, response.status_code)

        response = self.send_request(data={
            'email': fake_user.VALID_USERS[0]['email'],
            'current_password': 'newpassword1',
            'new_password': 'newpassword2'
        })
        self.assertEquals(200, response.status_code)

        response = self.send_request(data={
            'email': fake_user.VALID_USERS[0]['email'],
            'current_password': 'newpassword2',
            'new_password': 'newpassword3'
        })
        self.assertEquals(200, response.status_code)

        response = self.send_request(data={
            'email': fake_user.VALID_USERS[0]['email'],
            'current_password': 'newpassword3',
            'new_password': 'newpassword4'
        })
        self.assertEquals(200, response.status_code)

        response = self.send_request(data={
            'email': fake_user.VALID_USERS[0]['email'],
            'current_password': 'newpassword4',
            'new_password': 'newpassword5'
        })
        self.assertEquals(200, response.status_code)

        response = self.send_request(data={
            'email': fake_user.VALID_USERS[0]['email'],
            'current_password': 'newpassword5',
            'new_password': 'newpassword1'
        })
        self.assertEquals(401, response.status_code)
        res_data = json.loads(response.data)
        custom_code = res_data['custom_code']
        self.assertEquals(custom_code, 'pass_diff')

        response = self.send_request(data={
            'email': fake_user.VALID_USERS[0]['email'],
            'current_password': 'newpassword5',
            'new_password': 'newpassword6'
        })
        self.assertEquals(200, response.status_code)
