from urllib.parse import urljoin

from attrdict import AttrDict

from ..errors import MethodNotImplemented


class BaseResource(AttrDict):

    url = None
    prop_types = {}
    json_id_keys = []

    def __init__(self, api):
        super().__init__()
        self.api = api

    @classmethod
    def method_not_implemented(cls, method):
        raise MethodNotImplemented(method, cls.url)

    def retrieve(self, ep_id):
        resp = self.api.get(urljoin(self.url, ep_id))
        return self(resp)
    #
    # @classmethod
    # def all(cls, api_key=None, **params):
    #     requestor = Requestor(api_key)
    #     url = cls.class_url()
    #     response, api_key = requestor.request('get', url, params)
    #     return convert_to_easypost_object(response, api_key)
    #
    # def _ident(self):
    #     return [self.get('id')]
    #
    # def refresh(self):
    #     requestor = Requestor(self.api_key)
    #     url = self.instance_url()
    #     response, api_key = requestor.request('get', url, self._retrieve_params)
    #     self.refresh_from(response, api_key)
    #     return self
    #
    # def save(self):
    #     if self._unsaved_values:
    #         requestor = Requestor(self.api_key)
    #         params = {}
    #         for k in self._unsaved_values:
    #             params[k] = getattr(self, k)
    #             if type(params[k]) is EasyPostObject:
    #                 params[k] = params[k].flatten_unsaved()
    #         params = {self.class_name(): params}
    #         url = self.instance_url()
    #         response, api_key = requestor.request('put', url, params)
    #         self.refresh_from(response, api_key)
    #
    #     return self
    #
    # def delete(self, **params):
    #     requestor = Requestor(self.api_key)
    #     url = self.instance_url()
    #     response, api_key = requestor.request('delete', url, params)
    #     self.refresh_from(response, api_key)
    #     return self

    # def instance_url(self):
    #     easypost_id = self.get('id')
    #     if not easypost_id:
    #         raise Error('%s instance has invalid ID: %r' % (type(self).__name__, easypost_id))
    #     easypost_id = Requestor._utf8(easypost_id)
    #     base = self.class_url()
    #     param = quote_plus(easypost_id)
    #     return '{base}/{param}'.format(base=base, param=param)
    #
