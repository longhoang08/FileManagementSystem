import email_validator


def validate_email(email):
    try:
        email_validator.validate_email(email)  # validate and get info
    except email_validator.EmailNotValidError:
        return False
    return True


def validate_password(password):
    return len(password) >= 8 and len(password) <= 100 and password.replace(' ', '').isalnum()


def validate_fullname(fullname):
    return len(fullname) >= 8 and len(fullname) <= 100 and fullname.replace(' ', '').isalpha()


def validate_username(username):
    return len(username) >= 6 and len(username) <= 20 and username.replace(' ', '').isalnum()


def validate_register(username, email, fullname, password):
    return (validate_username(username) and
            validate_email(email) and
            validate_fullname(fullname) and
            validate_password(password))
