# Import marshmallow for light weight serialization & de-serialization
from marshmallow import Schema, fields, post_load, post_dump

# Import jsonschema for Schema validation
from jsonschema import validate, exceptions

# Import JSON for JavaScript Object Notation serialization
import json

class Notification(object):

    # Define the schema as a class level variable
    file_handle = open('notifications/resources/Notification_Schema.json', 'r')
#    file_handle = open('Notification_Schema.json', 'r')
    __schema__ = json.load(file_handle)
    file_handle.close()
#    __schema__ = {
#        "$schema":"http://json-schema.org/draft-04/schema#",
#        "title":"Notification",
#        "description":"A Notification object",
#        "type": "object",
#        "properties": {
#            "sensitivity": 
#                {
#                  "type": "string"
#                 ,"description":"Sensitivity of the notification"
#                }, 
#            "note": 
#                {
#                 "type": "string"
#                 ,"description":"The notification text"
#                }, 
#            "id": 
#                {
#                 "type": "number"
#                 ,"description":"The identifier (read only)"
#                }, 
#            "action": 
#                {
#                 "type": "string"
#                 ,"description":"What action is taken when the notification is selected"
#                }
#            },
#        "required":["action", "note"]
#    }

    # Define the Marshmallow shcema
    class Notification_Schema(Schema):
        sensitivity = fields.String(required=False)

        class Meta:
            fields = ("id","note","action")

        @post_dump()
        def wrapper(self, data):
            return { 'notification' : data }

    # Class initializer
    def __init__(self
                ,note=None
                ,action=None
                ,sensitivity=None):
        self.id = -1
        self.related_links = []
        self.note = note
        self.action = action
        self.sensitivity = sensitivity

    # Class representation when used with repr(x) or str(x)
    def __repr__(self):
        return 'Notification(<id={self.id!r}>)'.format(self=self)

    # Class representation as a string when used with str(x)
    def __str__(self):
        return_string = 'Notification '+str(self.id)+'; '
        return_string += 'note: '+self.note + ', '
        return_string += 'action: '+self.action + ', '
        return_string += 'sensitivity: '+self.sensitivity + ', '
        return return_string

    def dump(self):
        data_string = None
        return_string = None

        # Create a private instance of the schema
        __n_schema = self.Notification_Schema(many=False)

        # create the serialized data in JSON using the schema
        # note, for json.loads to work successfully, the ' characters in 
        # the schema output are replaced with "
        #
        data_string = str(__n_schema.dump(self).data).replace('None','null')
        return_string = data_string.replace("'",'"')

        return return_string

    def load(self, json_data, strict=False):
        try:
            # Load the provided JSON string into a dict
            __json_data = json.loads(json_data)

            # Step 1 - Validate the JSON data against the schema
            validate(__json_data['notification'], self.__schema__)

            # Step 2 - Use marshmallow to deserialize
            __n_schema = self.Notification_Schema(many=False, strict=True)
            __result = __n_schema.load(__json_data['notification']).data

            # Step 3 - Update this object to the values loaded from the JSON data.
            #          Note that the ID is ignored.
            if 'note' in __result:
                self.note = __result['note']

            if 'action' in __result:
                self.action = __result['action']

            if 'sensitivity' in __result:
                self.sensitivity = __result['sensitivity']
        except exceptions.ValidationError as v:
#            print('A validation error occured: ', v.message)
            raise exceptions.ValidationError('A validation error occured: ' + v.message)
        except Exception as e:
            print('An unknown exception occured : {0}'.format(str(e)))

        return

    def iter_fields(self):
        yield "ID", self.id
        yield "note", self.note
        yield "action", self.action
        yield "sensitivity", self.sensitivity

