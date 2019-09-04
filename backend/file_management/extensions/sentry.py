# coding=utf-8

from file_management import BadRequestException, UnAuthorizedException, \
    ForbiddenException, NotFoundException


def before_send(event, hint):
    """
    Ignore custom exception
    """
    if 'exc_info' in hint:
        exc_type, exc_value, tb = hint['exc_info']
        if isinstance(exc_value, (
                BadRequestException, UnAuthorizedException, ForbiddenException,
                NotFoundException)):
            return None
    return event
