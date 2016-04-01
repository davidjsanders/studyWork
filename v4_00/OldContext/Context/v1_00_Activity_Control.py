from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Context import Control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class v1_00_Activity_Control(object):
    __controller = None

    def __init__(self):
        self.module_name = 'v1_00_Activity_Control'
        self.method_name = 'unknown'
        self.controller = Control.global_controller

    def activity_request_all(self):
        self.method_name = 'activity_request_all'
        try:
            self.controller.log('{0}-{1}: Activities request received.'\
                .format(self.module_name,
                        self.method_name)
            )

            success = 'success'
            status = '200'
            message = 'Activity'
            data = {"activities":[
                      {"activity":"value"}
                   ]}

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

        self.controller.log('{0}-{1}: Activities request returned: {2}'\
            .format(self.module_name,
                    self.method_name,
                    data)
        )

        return return_value


    def update_activity(
        self,
        activity=None,
        json_string=None
    ):
        self.method_name = 'update_activity'
        try:
            success = 'success'
            status = '200'
            message = 'Sample'
            data = None

            self.controller.log('{0}-{1}: Activity update request received.'\
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

            description=json_data['description']
            self.controller.log('{0}-{1}: Description provided: {2}'\
                .format(self.module_name,
                        self.method_name,
                        description)
            )

            state=json_data['state']
            if not type(state) == bool:
                raise KeyError('State must be provided as a boolean - true '+\
                               'or false')
            self.controller.log('{0}-{1}: State provided: {2}'\
                .format(self.module_name,
                        self.method_name,
                        state)
            )

            # Do whatever updates need done.
            data = {"activity":activity,
                    "description":description,
                    "state":state}
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

        self.controller.log('{0}-{1}: Activity update request returned: {2}'\
            .format(self.module_name,
                    self.method_name,
                    data)
        )

        return return_value

    def old_update_activity(
        self,
        activity=None,
        json_string=None
    ):
        self.method_name = 'update_activity'

        try:
            success = 'success'
            status = 200
            message = 'Update activity request'
            data = None

            self.controller.log('{0}-{1}: Activities request received.'\
                .format(self.module_name,
                        self.method_name)
            )

            if not type(json_string) == str:
                raise KeyError('JSON data was not provided as '+\
                               'a string')
            if json_string in (None, ''):
                raise KeyError('No JSON data was provided, so '+\
                               'there were no keys')

            if not type(activity) == str:
                raise KeyError('Activity was not provided as '+\
                               'a string')
            if activity in (None, '', []):
                raise KeyError('No JSON data was provided, so '+\
                               'there were no keys')

            loading_json = True
            json_data = json.loads(json_string)
            loading_json = False

            key=json_data['key']
            if (not type(key) == str) \
            or (not key == '1234-5678-9012-3456'):
                raise ValueError('Key is incorrectly formed or incorrect')
            self.controller.log('{0}-{1}: Key was provided correctly.'\
                .format(self.module_name, method_name))

            description=json_data['description']
            self.controller.log('{0}-{1}: Got description={2}.'\
                .format(self.module_name, method_name, description))

            state=json_data['state']
            if not type(state) == bool:
                raise KeyError('State must be provided as a boolean - true '+\
                               'or false')
            self.controller.log('{0}-{1}: Got state={2}.'\
                .format(self.module_name, method_name, state))

        except KeyError as ke:
            success = 'error'
            status = 400
            message = 'Key Error: {0}'.format(str(ke))
            data = {'error-message':message}
            self.controller.log('{0}-{1}: {2}'\
                .format(self.module_name, method_name,message))
        except ValueError as ke:
            success = 'error'
            status = 403
            message = 'Value Error: {0}'.format(str(ke))
            if loading_json:
                status = 400
                message = 'The JSON data is badly formed. Please check'
            data = {'error-message':message}
            self.controller.log('{0}-{1}: {2}'\
                .format(self.module_name, method_name,message))
        except Exception as e:
            success = 'error'
            status = 500
            message = 'Exception: {0}'.format(repr(e))
            data = {'error-message':message}
            self.controller.log('{0}-{1}: {2}'\
                .format(self.module_name, method_name, message))


        self.controller.log('{0}-{1}: PUT Completed.'\
            .format(self.module_name, method_name))

        return_value = self.controller.do_response(message=message,
                                                   data=data,
                                                   status=status,
                                                   response=success)

        return return_value
