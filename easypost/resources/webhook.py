from voluptuous import Schema

from .base import BaseResource


class Webhook(BaseResource):

    url = 'webhooks'
    key = 'webhook'

    prop_types = Schema({
        "id": str,
        "object": str,
        "mode": str,
        "url": str,
        "disabled_at": str,  # FIXME: should be a datetime?
    })
