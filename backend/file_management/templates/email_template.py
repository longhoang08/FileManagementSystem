# coding=utf-8
import logging
import os

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def gen_confirm_email_body_template(fullname, username, active_link):
    msg_html = ('<p>Hello {},</p>' + os.linesep +
                '<p>You are almost ready to start using Login app with handle {}.</p>' + os.linesep +
                '<p>Simply click <a href="' + active_link + '">link</a> to verify your accout!</p>' + os.linesep +
                os.linesep +
                '<p>Best regards,</p>' + os.linesep +
                "<p>File management system team</p>")
    return msg_html.format(fullname, username)
