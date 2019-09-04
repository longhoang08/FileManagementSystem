from flask import request
from flask_restplus.reqparse import RequestParser as BaseRequestParser
from werkzeug.exceptions import BadRequest

from file_management.extensions.exceptions import BadRequestException


class RequestParser(BaseRequestParser):
    def parse_args(self, req=None, strict=False):
        """
        Parse all arguments from the provided request and return
        the results as a ParseResult.
        if req includes args not in parser, throw 400 BadRequest exception
        """
        if req is None:
            req = request

        result = self.result_class()

        req.unparsed_arguments = dict(
            self.argument_class('').source(req)) if strict else {}
        errors = {}
        for arg in self.args:
            value, found = arg.parse(req, self.bundle_errors)
            if isinstance(value, ValueError):
                errors.update(found)
                found = None
            if found or arg.store_missing:
                result[arg.dest or arg.name] = value
        if errors:
            raise BadRequestException('Input payload validation failed', errors)

        if strict and req.unparsed_arguments:
            arguments = ', '.join(req.unparsed_arguments.keys())
            msg = 'Unknown arguments: {0}'.format(arguments)
            raise BadRequest(msg)

        return result
