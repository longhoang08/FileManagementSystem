# coding=utf-8
from flask_restplus import fields

register_user_req = {
    'email': fields.String(required=True, description='user email address'),
    'username': fields.String(required=True, description='user username'),
    'fullname': fields.String(required=True, description='fullname of user'),
    'password': fields.String(required=True, description='user password'),
}

login_req = {
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password'),
}

login_google_req = {
    'token': fields.String(required=True, description='Google login token'),
}

change_password_req = {
    'email': fields.String(required=True, description='email'),
    'current_password': fields.String(required=True, description='current password'),
    'new_password': fields.String(required=True, description='new password')
}

download_file_req = {
    'user_id': fields.Integer(required=True, description='User want to download files'),
    'file_id': fields.String(required=True, description='File_id')

}
file_details_req = {
    'file_id': fields.String(required=False, description='File_id'),
    'q': fields.String(required=False, description='Search text'),
    'user_id': fields.String(required=False, description='Search text'),
    'basic_info': fields.Boolean(required=False, description='Only get basic info of file')
}

folder_details_req = {
    'folder_id': fields.String(required=False, description='folder_id')
}

folder_create_req = {
    'parent_id': fields.String(required=False, description='parent_id'),
    'folder_name': fields.String(required=False, description='folder_name')
}