# coding=utf-8
from flask_restplus import fields

from file_management.api import api

user_res = {
    'email': fields.String(description='user email address'),
    'username': fields.String(description='user username'),
    'fullname': fields.String(description='fullname of user'),
    'avatar_url': fields.String(description='avatar url of user'),
}

pending_register_res = {
    'username': fields.String(description="Username"),
    'email': fields.String(description="Email"),
    'fullname': fields.String(description="User full name"),
}

log_field = api.model('log', {
    'message' : fields.String(description="Message"),
    'created_at': fields.DateTime(description="Created at")
})

notification_field = api.model('notification', {
    'message' : fields.String(description="Message"),
    'created_at': fields.DateTime(description="Create at")
})

file_uploaded_res = {
    'file_id': fields.String(required=True, description="File id"),
    'file_title': fields.String(required=True, description="File's name"),
    'file_size': fields.Integer(required=True, description="Filesize"),
    'parent_id': fields.String(required=True, description="Parent folder's id"),
    'user_id': fields.Integer(required=True, description="Owner id"),
    'mime_type' : fields.String(required=True, description="MIME Type"),
    'starred' : fields.Boolean(required=True, description="Is starred"),
    'trashed' : fields.Boolean(required=True, description="Is trashed"),
    'trashed_time' : fields.DateTime(description="Trashed date"),
    'version' :fields.Integer(required=True, description="Version"),
    'has_thumbnail' : fields.Boolean(required=True, description="Is Has thumbnail"),
    'thumbnail_url' : fields.String(required=True, description="Thumbnail url"),
    'shared' : fields.Boolean(required=True, description="Is shared")
} 


