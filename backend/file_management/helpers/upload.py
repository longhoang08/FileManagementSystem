import uuid
import mimetypes
from file_management.constant import link

def generate_file_id(user_id):
    """Generate unique file_id """
    randomString = uuid.uuid4().hex
    randomString  = randomString.upper() 
    return user_id + '-' + randomString
    
def get_mime_type(file_name):
    return mimetypes.MimeTypes().guess_type(file_name)[0]

def is_has_thumbail(file_name):
    return get_mime_type(file_name) != None

#TODO 
def get_thumbnail_url(file_name):
    if not is_has_thumbail(file_name):
        return link.DEFAULT_THUMBNAIL
    else:
        return "that's thumbnail_url"