from file_management import repositories
from file_management.helpers.password import hash_password

VALID_USERS = [
    {
        "email": "test01@coin-mail.com",
        "username": "account1",
        "fullname": "Account one",
        "password": "12345678"
    },
    {
        "email": "test02@testmail.com",
        "username": "account2",
        "fullname": "Account two",
        "password": "12345678"
    },
    {
        "email": "test03@testmail.com",
        "username": "account3",
        "fullname": "Account three",
        "password": "12345678"
    }
]


def insert_some_user_to_db_for_testing():
    for register in VALID_USERS:
        repositories.user.save_user_to_database(
            username=register['username'],
            email=register['email'],
            fullname=register['fullname'],
            password=hash_password(register['password']),
        )
    for register in VALID_USERS:
        assert (repositories.user.find_one_by_username(register['username']) != None)


def insert_some_register_to_db_for_testing():
    for register in VALID_USERS:
        repositories.pending_register.save_pending_register_to_database(**register)
    for register in VALID_USERS:
        assert (repositories.pending_register.find_one_by_username(register['username']) != None)
