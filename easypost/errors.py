class HttpError(Exception):
    message = ('Unexpected error communicating with EasyPost. If this '
               'problem persists please let us know at contact@easypost.com.')

    def __init__(self, message=''):
        super(HttpError, self).__init__(message or self.message)


class ApiError(Exception):
    def __init__(self, response, message=None):
        super(ApiError, self).__init__(message)
        status_code = response.status_code
        try:
            json = response.json()
        except ValueError:
            raise Exception('Status: <{}> JSON response from API could not be decoded.'.format(status_code))  # FIXME: is this useful? should i just let it raise its own exception?

        try:
            error = json['error']  # FIXME: not confident that this is the best way to access errors
            raise Exception(error.get('message', ''))
        except KeyError:
            raise Exception('Invalid response from API: <{}> {}'.format(status_code, json))


class NoApiKeyError(Exception):
    message = (
        'No API key provided. Set an API key via `easypost.api_key = \'APIKEY\'`. Your API keys '
        'can be found in your EasyPost dashboard, or you can email us at contact@easypost.com '
        'for assistance.')

    def __init__(self, message=''):
        super(NoApiKeyError, self).__init__(message or self.message)


class MethodNotImplemented(Exception):
    message = 'Method "{}" not implemented for endpoint {}'

    def __init__(self, method, endpoint):
        super(MethodNotImplemented, self).__init__(self.message.format(method, endpoint))
