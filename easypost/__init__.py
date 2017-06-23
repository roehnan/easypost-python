from urllib.parse import urljoin

import requests

from .version import VERSION
from .errors import ApiError, HttpError, NoApiKeyError
from .resources.webhook import Webhook


__author__ = 'EasyPost <oss@easypost.com>'
__version__ = VERSION
version_info = tuple(int(v) for v in VERSION.split('.'))
USER_AGENT = 'EasyPost/v2 PythonClient/{0}'.format(VERSION)  # FIXME: not all endpoints are /v2 anymore
api_key = None
api_base = 'https://api.easypost.com/v2'  # FIXME: not all endpoints are /v2 anymore
request_lib = 'requests'  # FIXME: need to support google.appengine.api. will do that as the last step
timeout = 60


class Api:

    DEFAULT_HEADERS = {
        'X-Client-User-Agent': {
            'client_version': VERSION,
            'lang': 'python',
            'publisher': 'easypost',
            'request_lib': request_lib,
        },
        'User-Agent': USER_AGENT,
        'Authorization': 'Bearer %s' % api_key,
        'Content-type': 'application/json'  # FIXME: changed from application/x-www-form-urlencoded
    }

    @classmethod
    def handle_api_error(cls, response):
        if not (200 <= response.status_code < 300):
            raise ApiError(response)

    @classmethod
    def build_url(cls, path):
        return urljoin(api_base, path)

    @classmethod
    def build_headers(cls, headers):
        headers = headers or {}
        if not api_key:  # FIXME: we currently allow Users to be created without an api_key. do we want to continue allowing that?
            raise NoApiKeyError()
        return {**cls.DEFAULT_HEADERS, **headers}

    @classmethod
    def request(cls, method, path, params, headers):
        data = None
        if method == 'POST' or method == 'PUT':
            data = params
            params = None
        url = cls.build_url(path)
        headers = cls.build_headers(headers)

        try:
            resp = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                data=data,
                timeout=timeout,
                verify=True
            )
        except Exception:
            raise HttpError()

        cls.handle_api_error(resp)
        return resp.json()  # FIXME: this is only safe if ApiError has already run .json()

    @classmethod
    def get(cls, path, params, headers):
        return cls.request('GET', path, params, headers)

    @classmethod
    def post(cls, path, params, headers):
        return cls.request('POST', path, params, headers)

    @classmethod
    def put(cls, path, params, headers):
        return cls.request('PUT', path, params, headers)

    @classmethod
    def patch(cls, path, params, headers):
        return cls.request('PATCH', path, params, headers)

    @classmethod
    def delete(cls, path, params, headers):
        return cls.request('DELETE', path, params, headers)
