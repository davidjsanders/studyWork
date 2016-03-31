from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Test import Control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class v1_00_Sample_Control(object):
    __controller = None

    def __init__(self):
        self.controller = Control.global_controller
        self.module_name = 'Test'
        self.method_name = 'unknown'

    def sample_request(self):
        self.method_name = 'sample_request'
        try:
            success = 'success'
            status = '200'
            message = 'Sample'
            data = {"sample":"value"}

            self.controller.log('{0}-{1}: Sample request received.'\
                .format(self.module_name,
                        self.method_name)
            )
        except Exception as e:
            success = 'error'
            status = '500'
            message = '{0}-{1}: {2}'\
                .format(self.module_name,
                        self.method_name,
                        repr(e))
            data = {"exception":repr(e)}
            self.controller.log(message)
            print(error_text)

        return_value = self.controller.do_response(message=message,
                                                   data=data,
                                                   status=status,
                                                   response=success)

        self.controller.log('{0}-{1}: Sample request returned: {2}'\
            .format(self.module_name,
                    self.method_name,
                    data)
        )

        return return_value

    def sample_update(
        self,
        json_string=None
    ):
        self.method_name = 'sample_update'
        try:
            success = 'success'
            status = '200'
            message = 'Sample'
            data = None

            self.controller.log('{0}-{1}: Sample update request received.'\
                .format(self.module_name,
                        self.method_name)
            )

            # Validate the raw data is valid
            if not type(json_string) == str:
                raise KeyError('JSON data was not provided as '+\
                               'a string')

            self.controller.log('{0}-{1}: JSON data is a string.'\
                .format(self.module_name,
                        self.method_name)
            )

            if json_string in (None, ''):
                raise KeyError('No JSON data was provided, so '+\
                               'there were no keys')

            self.controller.log('{0}-{1}: JSON string is not empty.'\
                .format(self.module_name,
                        self.method_name)
            )

            # Set a sentinel around loading the JSON data so we know if it's
            # poorly formatted and can catch it in the exception.
            self.controller.log('{0}-{1}: Loading JSON'\
                .format(self.module_name,
                        self.method_name)
            )

            loading_json = True
            json_data = json.loads(json_string)
            loading_json = False

            self.controller.log('{0}-{1}: JSON is valid and loaded.'\
                .format(self.module_name,
                        self.method_name)
            )

            # Get the key. Repeat this approach for all parameters.
            key=json_data['key']

            # Validate the key
            if (not type(key) == str) \
            or (not key == '1234-5678-9012-3456'): # Change to correct key!
                raise ValueError('Key is incorrectly formed or incorrect')

            self.controller.log('{0}-{1}: Key was correct.'\
                .format(self.module_name,
                        self.method_name)
            )

            # Do whatever updates need done.
            data = {"sample":"updated-value"}
        except KeyError as ke:
            success = 'error'
            status = 400
            message = '{0}-{1}: Key Error >> {2}'\
                .format(self.module_name, self.method_name, str(ke))
            data = {'error-message':str(ke)}
            self.controller.log(message)
        except ValueError as ve:
            success = 'error'
            status = 403
            message = '{0}-{1}: {2}'\
                .format(self.module_name, self.method_name, str(ve))
            data = {'error-message':str(ve)}
            if loading_json:
                status = 400
                message = '{0}-{1}: {2}'\
                    .format(self.module_name,
                            self.method_name,
                            'The JSON data is badly formed. Please check')
                data = {'error-message':'Bad JSON data'}
            self.controller.log(message)
        except Exception as e:
            success = 'error'
            status = '500'
            message = '{0}-{1}: {2}'\
                .format(self.module_name,
                        self.method_name,
                        repr(e))
            data = {"exception":repr(e)}
            self.controller.log(message)
            print(error_text)

        return_value = self.controller.do_response(message=message,
                                                   data=data,
                                                   status=status,
                                                   response=success)

        self.controller.log('{0}-{1}: Sample update request returned: {2}'\
            .format(self.module_name,
                    self.method_name,
                    data)
        )

        return return_value


