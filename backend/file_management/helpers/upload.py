import uuid

def generate_file_id(user_id):
    """Generate unique file_id """
    randomString = uuid.uuid4().hex
    randomString  = randomString.upper() 
    return user_id + '-' + randomString
