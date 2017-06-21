class Report(AllResource, CreateResource):

    @classmethod
    def create(cls, api_key=None, **params):
        requestor = Requestor(api_key)
        url = "%s/%s" % (cls.class_url(), params['type'])
        wrapped_params = {cls.class_name(): params}

        response, api_key = requestor.request('post', url, wrapped_params, False)
        return convert_to_easypost_object(response, api_key)

    @classmethod
    def all(cls, api_key=None, **params):
        requestor = Requestor(api_key)
        url = "%s/%s" % (cls.class_url(), params['type'])
        response, api_key = requestor.request('get', url, params)
        return convert_to_easypost_object(response, api_key)
