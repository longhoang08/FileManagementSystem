# coding=utf-8
import logging

__author__ = 'Dang'
_logger = logging.getLogger(__name__)


def gen_confirmed_template(fullname, username, active_link):
    msg_html = ("""<!DOCTYPE html>
<html>
<head>
  <meta http-equiv='refresh' content='2; URL=http://ufile.ml/'>
</head>
<body>
   <h2>Welcome to Ufile, {}</h2>
<h3>Please wait a moment...</h3>
</body>
</html>""")
    msg_html = msg_html.format(fullname)
    # msg_html = msg_html.replace("'", '"')
    return msg_html
