from .base import BaseResource


class Webhook(BaseResource):
    def update(self, **params):
        requestor = Requestor(self.api_key)
        url = self.instance_url()
        response, api_key = requestor.request('put', url, params)
        self.refresh_from(response, api_key)
        return self
