from urllib.parse import urljoin

import requests

from .version import VERSION
from .errors import Error
from .resources.webhook import Webhook


__author__ = 'EasyPost <oss@easypost.com>'
__version__ = VERSION
version_info = tuple(int(v) for v in VERSION.split('.'))
USER_AGENT = 'EasyPost/v2 PythonClient/{0}'.format(VERSION)
api_key = None
api_base = 'https://api.easypost.com/v2'
request_lib = 'requests'  # FIXME: we have supported other libs. do we still need to?
timeout = 60


class API:

    DEFAULT_HEADERS = {
        'X-Client-User-Agent': {
            'client_version': VERSION,
            'lang': 'python',
            'publisher': 'easypost',
            'request_lib': request_lib,
        },
        'User-Agent': USER_AGENT,
        'Authorization': 'Bearer %s' % api_key,
        'Content-type': 'application/json' # FIXME: changed from application/x-www-form-urlencoded
    }

    @classmethod
    def handle_api_error(cls, response):  # FIXME: should this be in a different class/file?
        status_code = response.status_code
        resp_text = response.text
        if not (200 <= status_code < 300):
            try:
                error = response['error']
            except (KeyError, TypeError):
                raise Error("Invalid response from API: (%d) %r " % (status_code, resp_text), status_code, resp_text)

            try:
                raise Error(error.get('message', ''), status_code, resp_text)
            except AttributeError:
                raise Error(error, status_code, resp_text)

    @classmethod
    def build_url(cls, path):
        return urljoin(api_base, path)

    @classmethod
    def build_headers(cls, headers):
        headers = headers or {}
        if not api_key:  # FIXME: we currently allow Users to be created without an api_key
            raise Error(  # FIXME: should i start making better error classes like NoApiKeyError()?
                'No API key provided. Set an API key via "easypost.api_key = \'APIKEY\'. '
                'Your API keys can be found in your EasyPost dashboard, or you can email us '
                'at contact@easypost.com for assistance.')
        return {**cls.DEFAULT_HEADERS, **headers}

    @classmethod
    def request(cls, method, path, params, headers):
        data = None
        if method == 'post' or method == 'put':
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
            raise Error("Unexpected error communicating with EasyPost. If this "
                    "problem persists please let us know at contact@easypost.com.")

        cls.handle_api_error(resp)  # FIXME: should i put this all in the "try:" block?
        return resp.json()  # FIXME: can i assume that this is safe?

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
