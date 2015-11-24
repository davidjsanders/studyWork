# Import marshmallow for light weight serialization & de-serialization
from marshmallow import Schema, fields, post_load, post_dump

# Import jsonschema for Schema validation
from jsonschema import validate, exceptions, Draft3Validator

# Import JSON for JavaScript Object Notation serialization
import json

class Notification(object):
    __schema_filename__ = 'schemas/Notification_Schema.json'

    # Define the schema as a class level variable
    # and load the schema from disk
    file_handle = open(__schema_filename__, 'r')
    __schema__ = json.load(file_handle)
    file_handle.close()

    # Define the Marshmallow shcema
    class Notification_Schema(Schema):
        note = fields.String(required=True)
        action = fields.String(required=True)
        sensitivity = fields.String(required=False)
        identifier = fields.Integer(required=True)

        #The post dump decorator ensures the function wrapper is called
        #every time a Notification is dumped. It wrapps the JSON data in an
        #'envelope' with the key 'notification'.
        @post_dump()
        def wrapper(self, data):
            return { 'notification' : data }

    # Class initializer
    def __init__(self
                ,note=None
                ,action=None
                ,sensitivity=None
                ,identifier=None):
        self.identifier = (identifier or -1) #If not provided, set it to -1
        #self.related_links = []
        self.note = note
        self.action = action
        if sensitivity != None \
        and sensitivity in ['low', 'normal', 'high']:
            self.sensitivity = sensitivity
        elif sensitivity == None:
            self.sensitivity = None
        else:
            self.sensitivity = 'normal'

    # Class representation when used with repr(x) or str(x)
    def __repr__(self):
        return 'Notification(<identifier={self.identifier!r}>)'.format(self=self)

    # Class representation as a string when used with str(x)
    def __str__(self):
        return_string = 'Notification '+(str(self.identifier or -1))+'; '
        return_string += 'note: "'+ (self.note or 'None') + '", '
        return_string += 'action: "'+ (self.action or 'None') + '", '
        return_string += 'sensitivity: "'+ (self.sensitivity or 'None') + '". '
        return return_string

    def dump(self):
        # Create a variable for the return element
        return_string = None

        # Create a private instance of the schema
        __n_schema = self.Notification_Schema(many=False)

        # create the serialized data in JSON using the schema
        # note, for json.loads to work successfully, the ' characters in 
        # the schema output are replaced with " and references to None are
        # replaced with null. Python's json package does this by default BUT
        # marshmallow does NOT.
        #
        return_string = str(__n_schema.dump(self).data)\
            .replace('None','null')\
            .replace("'",'"')

        return return_string

    def load(self, json_data, strict=False):
        __temp_json = json_data.replace("'",'"').replace('None','null')

        current_step = 0
        try:
            # Load the provided JSON string into a dict
            __json_data = json.loads(__temp_json)

            current_step += 1
            # Step 1 - Validate the JSON data against the schema
            #          An exception will be raised if there is an issue.
            validate(__json_data, self.__schema__)

            current_step += 1
            # Step 2 - Use marshmallow to deserialize the JSON data.
            __n_schema = self.Notification_Schema(many=False, strict=False)
            __result = __n_schema.load(__json_data['notification']).data

            current_step += 1
            # Step 3 - Update this object to the values loaded from JSON data.
            if 'identifier' in __result:
                self.identifier = __result['identifier']
            if 'note' in __result:
                self.note = __result['note']
            if 'action' in __result:
                self.action = __result['action']
            if 'sensitivity' in __result:
                self.sensitivity = __result['sensitivity']

        except exceptions.ValidationError as v:
            exception_string = 'Data issue: '
            exception_string += str(__json_data['notification']) + '; '
            exception_string += v.message + '.  '
            exception_string += 'The following fields are required and '
            exception_string += 'may not be null or None: '
            required_fields = self.__schema__['properties']['notification']['required']
            for idx2, key in enumerate(required_fields):
                exception_string += required_fields[idx2] + ' '
            exception_string += ''
#            exception_string = '\033[4mData issue\033[0m\n'
#            exception_string += '\033[93m' 
#            exception_string += str(__json_data['notification']) + '\033[0m\n'
#            exception_string += ' "\033[0m' + v.message + '"\033[0m\n'
#            exception_string += 'The following fields are required and '
#            exception_string += 'may not be null or None: '
#            required_fields = self.__schema__['properties']['notification']['required']
#            for idx2, key in enumerate(required_fields):
#                exception_string += '\033[4m'
#                exception_string += required_fields[idx2]
#                exception_string += '\033[0m '
#            exception_string += '\n'
            raise exceptions.ValidationError(exception_string)
        except Exception as e:
            print('An unknown exception occured at {1}: {0}'\
                  .format(str(e), current_step))

        return
