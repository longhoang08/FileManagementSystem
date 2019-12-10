import uuid
import mimetypes
from file_management.constant import link
from preview_generator.manager import PreviewManager
def generate_file_id(user_id):
    """Generate unique file_id """
    randomString = uuid.uuid4().hex
    randomString  = randomString.upper() 
    return user_id + '-' + randomString
    
def get_mime_type(file_name):
    """Get mimetype from file name. Str return should be "image/jpeg" """
    return mimetypes.MimeTypes().guess_type(file_name)[0]

def is_has_thumbail(file_name):
    """ """
    return get_mime_type(file_name) != None

def gen_thumbnail(file_id, path_upload):
    manager = PreviewManager("fake_HDD/" + path_upload, create_folder= True)
    path_to_preview_image = manager.get_jpeg_preview(path_upload + '/' + file_id, height=500,width=400)
    return path_to_preview_image
    # return "path_preview"

def get_thumbnail_url(file_id, file_name, path_upload):
    mime = get_mime_type(file_name)
    if not is_has_thumbail(file_name):
        return link.DEFAULT_THUMBNAIL
    elif "image" in mime:
        return gen_thumbnail(file_id, path_upload)
    elif "pdf" in mime:
        return link.PDF_THUMBNAIL
    elif "audio" in mime:
        return link.SOUND_THUMBNAIL
    elif 'zip' in  mime:
        return link.ZIP_THUMBNAIL
    elif 'text' in mime:
        return link.TEXT_THUMBNAIL
    else :
        return link.DEFAULT_THUMBNAIL