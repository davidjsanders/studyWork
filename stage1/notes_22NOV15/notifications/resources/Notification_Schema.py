from marshmallow_jsonapi import Schema, fields
import marshmallow
from notifications.resources.Notifications import Notification

# https://marshmallow-jsonapi.readthedocs.org/en/latest/quickstart.html#declaring-schemas
def dasherize(text):
    return text.replace('_','-')

class Notification_Schema(Schema):
    id = fields.Str(dump_only=True)
    note = fields.Str()
    action = fields.Str()
    sensitivity = fields.Str()

    related = fields.Relationship(
        self_url='{server}/notification/{id}',
        self_url_kwargs={'id': '<id>', 'server':'http://localhost:5000'},
        related_url='{server}/notifications/',
        related_url_kwargs={'server':'http://localhost:5000'},
#        many=True, include_data=True,
#        type_='Notification'
    )

    class Meta:
        type_ = 'Notification'
        strict = True
        inflect = dasherize
