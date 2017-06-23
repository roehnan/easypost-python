class Blob(AllResource, CreateResource):
    @classmethod
    def retrieve(cls, easypost_id, api_key=None, **params):
        try:
            easypost_id = easypost_id['id']
        except (KeyError, TypeError):
            pass

        requestor = Requestor(api_key)
        url = '%s/%s' % (cls.class_url(), easypost_id)
        response, api_key = requestor.request('get', url)
        return response['signed_url']
