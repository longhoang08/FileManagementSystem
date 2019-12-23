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
    'q': fields.String(required=False, description='Search text'),
    'file_id': fields.String(required=False, description='id of file to get details'),
    'basic_info': fields.Boolean(required=False, description='Only get basic info of file', default=False),
    'only_photo': fields.Boolean(required=False, description='Only get photo'),
    'star': fields.Boolean(required=False, description='Only get star'),
    'trash': fields.Boolean(required=False, description='Only get file in trash'),
    'share': fields.Boolean(required=False, description='Only get shared file with me'),
    '_limit': fields.Integer(required=False, description='Limit each page', default=12),
    '_page': fields.Integer(required=False, description='Page-th', default=1),
}

move_req = {
    'file_ids': fields.List(fields.String, required=True, description='ID\'s File'),
    'new_parent': fields.String(required=False, description='new parent id')
}

folder_details_req = {
    'folder_id': fields.String(required=True, description='folder_id'),
    '_limit': fields.Integer(required=False, description='Limit each page', default=12),
    '_page': fields.Integer(required=False, description='Page-th', default=1)
}

folder_create_req = {
    'parent_id': fields.String(required=True, description='parent_id'),
    'file_title': fields.String(required=True, description='folder_name'),

}
switch_block_user_req = {
    'email': fields.String(required=True, description='Email need to block')
}

share_req = {
    'file_id': fields.String(required=True, description='File_id'),
    'emails': fields.List(fields.String, required=False),
    'share_by_link': fields.Boolean(required=False, default=False),
    'private': fields.Boolean(required=False, default=False)
}

trash_req = {
    'file_ids': fields.List(fields.String, required=True)
}

star_req = {
    'file_id': fields.String(required=True)
}

rename_req = {
    'file_id': fields.String(required=True),
    'new_name': fields.String(required=True)
}

user_details_req = {
    'ids': fields.List(fields.String, required=True)
}

copy_req = {
    'file_ids': fields.List(fields.String, required=True, description='ID\'s File'),
    'new_parent': fields.String(required=False, description='new parent id')
}
