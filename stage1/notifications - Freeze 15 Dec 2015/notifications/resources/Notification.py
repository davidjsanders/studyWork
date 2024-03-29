# Import marshmallow for light weight serialization & de-serialization
from marshmallow \
    import Schema, fields, post_load, post_dump, pre_load, pre_dump

# Import jsonschema for Schema validation
from jsonschema import validate, exceptions, Draft3Validator
import notifications.resources.Config as Config

# Import JSON for JavaScript Object Notation serialization
import json

class Notification(object):
    # Define the schema as a class level variable
    # and load the schema from disk
    file_handle = open(Config.__schema_filename__, 'r')
    __schema__ = json.load(file_handle)
    file_handle.close()

    # Define the Marshmallow shcema
    class Notification_Schema(Schema):
        note = fields.String(required=True)
        action = fields.String(required=True)
        sensitivity = fields.Method('get_sensitivity')
        identifier = fields.Integer(required=True)

        def get_sensitivity(self, note):
            try:
                if type(self.context) == str:
                    return value
                elif type(self.context) == dict:
                    if 'pre-lollipop' in self.context:
                        return 'not applicable'
                    else:
                        return note.sensitivity
            except Exception as e:
                print('Exception: '+repr(e))
            return note.sensitivity

        # pre_dump is called before the data is serialized to JSON. At this
        # point, a check is made to see whether the device is an Android
        # Lollipop or later device - if it is, Android checks the sensitivity
        # of a notification and if it's high doesn't return it. This is
        # emulated below.
        @pre_dump()
        def validate_this(self, data):
            if type(self.context) == dict:
                if ('locked' in self.context and self.context['locked'])\
                and ('android' in self.context and self.context['android']):
                    if not data.sensitivity == None:
                        print('Got sensitivity :)')
                        print(str(data))
                        if data.sensitivity.upper() == 'HIGH':
                            raise exceptions.ValidationError('Will be ignored')


    # Class initializer
    def __init__(self
                ,note=None
                ,action=None
                ,sensitivity=None
                ,identifier=None):
        self.identifier = (identifier or -1) #If not provided, set it to -1
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

    def __set_context(self, schema=None, schema_context=None):
        try:
            if not schema_context == None\
            and not schema == None:
                if type(schema_context) == dict\
                or type(schema_context) == list\
                or type(schema_context) == str:
                    pass
    #                schema['context'] = {}
                else:
                    raise TypeError('Context is not dict, list, or string')

                if type(schema_context) == dict:
                    for key in schema_context:
                        schema.context[key] = schema_context[key]
                elif type(schema_context) == list:
                    for key in schema_context:
                        schema.context[key] = True
                elif type(schema_context) == str:
                    schema.context = schema_context
                else:
                    raise TypeError('Context is not dict, list, or string')
                return schema
        except Exception as e:
            print('Exception: '+repr(e))
            raise

    def dump(self, schema_context=None):
        # Create a variable for the return element
        return_string = None

        # Create a private instance of the schema
        __n_schema = self.Notification_Schema(many=False)
        self.__set_context(__n_schema, schema_context)

        if type(schema_context) == dict:
            if 'pre-lollipop' in schema_context\
            or not 'android' in schema_context:
                __n_schema = self.Notification_Schema(
                                 many=False,
                                 only=('identifier','note','action')
                             )


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

    def load(self, json_data, strict=False, schema_context=None):
        current_step = 0

        try:
            __temp_json = json_data.replace("'",'"').replace('None','null')

            # Load the provided JSON string into a dict
            __json_data = json.loads(__temp_json)

            current_step += 1
            # Step 1 - Validate the JSON data against the schema
            #          An exception will be raised if there is an issue.
            validate(__json_data, Notification.__schema__)

            current_step += 1
            # Step 2 - Use marshmallow to deserialize the JSON data.
#            if not 'notification' in __json_data:
#                raise exceptions.ValidationError('Object is not a notification')
#                abort(400, message='Not a notification object')
            __n_schema = self.Notification_Schema(many=False, strict=False)
            __n_schema.context = {}
            self.__set_context(__n_schema, schema_context)
            __result = __n_schema.load(__json_data).data

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
            exception_string = 'Data issue: ** '
            exception_string += str(__json_data) + ' **; '
            exception_string += v.message + '.  '
            exception_string += 'Fields expected are:'
            fields_expected = self.__schema__['properties'].keys()
            max_length = len(fields_expected) - 1
            for idx, key in enumerate(fields_expected):
                exception_string += ' ' + key
                exception_string += ',' if idx < max_length else '. '
            exception_string += 'Required fields are :'
            required_fields = self.__schema__['required']
            max_length = len(required_fields) - 1
            for idx, key in enumerate(required_fields):
                exception_string += ' ' + key
                exception_string += ',' if idx < max_length else '. '
            raise exceptions.ValidationError(exception_string)
        except Exception as e:
            raise Exception('An unknown exception occured at {1}: {0}'\
                  .format(str(e), current_step))

        return

