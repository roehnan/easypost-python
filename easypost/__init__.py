from .version import VERSION
from .resources.webhook import Webhook


__author__ = 'EasyPost <oss@easypost.com>'
__version__ = VERSION
version_info = tuple(int(v) for v in VERSION.split('.'))
USER_AGENT = 'EasyPost/v2 PythonClient/{0}'.format(VERSION)
