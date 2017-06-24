from urllib.parse import urljoin

import requests

from .version import VERSION
from .errors import ApiError, HttpError, NoApiKeyError
from .resources.webhook import Webhook


class Api:

    def __init__(self, api_key=None, api_base='https://api.easypost.com/v2'):
        self.user_agent = 'EasyPost/v2 PythonClient/{0}'.format(VERSION)  # FIXME: not all endpoints are /v2 anymore
        self.api_key = api_key
        self.api_base = api_base  # FIXME: not all endpoints are /v2 anymore
        self.request_lib = 'requests'  # FIXME: need to support google.appengine.api. will do that as the last step
        self.timeout = 60
        self.default_headers = {
            'X-Client-User-Agent': {
                'client_version': VERSION,
                'lang': 'python',
                'publisher': 'easypost',
                'request_lib': self.request_lib,
            },
            'User-Agent': self.user_agent,
            'Authorization': 'Bearer %s'.format(self.api_key),
            'Content-type': 'application/json'  # FIXME: changed from application/x-www-form-urlencoded
        }

        self.Webhook = Webhook(self)

    @classmethod
    def handle_api_error(cls, response):
        if not (200 <= response.status_code < 300):
            raise ApiError(response)

    def build_url(self, path):
        return urljoin(self.api_base, path)

    def build_headers(self, headers):
        headers = headers or {}
        if not self.api_key:  # FIXME: we currently allow Users to be created without an api_key. do we want to continue allowing that?
            raise NoApiKeyError()
        return {**self.default_headers, **headers}

    def request(self, method, path, params, headers):
        data = None
        if method == 'POST' or method == 'PUT':
            data = params
            params = None
        url = self.build_url(path)
        headers = self.build_headers(headers)

        try:
            resp = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                data=data,
                timeout=self.timeout,
                verify=True
            )
        except Exception:
            raise HttpError()

        self.handle_api_error(resp)
        return resp.json()  # FIXME: this is only safe if ApiError has already run .json()

    def get(self, path, params=None, headers=None):
        return self.request('GET', path, params, headers)

    def post(self, path, params=None, headers=None):
        return self.request('POST', path, params, headers)

    def put(self, path, params=None, headers=None):
        return self.request('PUT', path, params, headers)

    def patch(self, path, params=None, headers=None):  # FIXME seems like we don't use PATCH anywhere
        return self.request('PATCH', path, params, headers)

    def delete(self, path, params=None, headers=None):
        return self.request('DELETE', path, params, headers)
