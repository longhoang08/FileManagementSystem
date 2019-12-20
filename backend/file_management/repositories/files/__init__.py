from file_management.repositories.file import FileElasticRepo
from . import delete, insert, update, utils

es = FileElasticRepo().es
