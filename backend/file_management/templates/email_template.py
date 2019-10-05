# coding=utf-8
import logging

__author__ = 'LongHB'
_logger = logging.getLogger(__name__)


def gen_confirm_email_body_template(fullname, username, active_link):
    msg_html = ('<p>Hello {},</p>'
                '<p>You are almost ready to start using uFile with handle {}.</p>'
                "<p>Simply click <a href= '{}' >link</a> to verify your accout!</p>"
                '<p>Best regards,</p>'
                "<p>uFile team</p>")
    msg_html = msg_html.format(fullname, username, active_link)
    # msg_html = msg_html.replace("'", '"')
    return msg_html
