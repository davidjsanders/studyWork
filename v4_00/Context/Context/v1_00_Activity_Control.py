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
        self.module_name = 'Activity_Control'
        self.controller = Control.global_controller

    def activity_request_all(self):
        try:
            self.controller.log('Activities request received.')

            success = 'success'
            status = '200'
            message = 'Activity'
            data = {"activities":[
                      {"activity":"value"}
                   ]}

        except Exception as e:
            success = 'error'
            status = '500'
            message = 'An error occurred.'
            error_text = 'v1_00_Activity_Control.activity_request_all: '+\
                'Exception {0}'.format(repr(e))
            data = {"exception":error_text}
            print(error_text)

        return_value = self.controller.do_response(message=message,
                                                   data=data,
                                                   status=status,
                                                   response=success)

        self.controller.log('Activities request returned {0}'.format(data))

        return return_value


    def update_activity(
        self,
        activity=None,
        json_string=None
    ):
        method_name='update_activity'
        self.controller.log('{0}-{1}: PUT received.'\
            .format(self.module_name, method_name))

        success = 'success'
        status = 200
        message = 'Update activity request'
        data = None

        try:
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
                .format(self.module_name, method_name,message))


        self.controller.log('{0}-{1}: PUT Completed.'\
            .format(self.module_name, method_name))

        return_value = self.controller.do_response(message=message,
                                                   data=data,
                                                   status=status,
                                                   response=success)

        return return_value
