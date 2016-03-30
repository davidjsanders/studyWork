from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Context import Control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class v1_00_Sample_Control(object):
    __controller = None

    def __init__(self):
        self.controller = Control.global_controller
        self.module_name = 'v1_00_Sample_Control'
        self.method_name = 'unknown'

    def sample_request(self):
        try:
            self.controller.log('{0}-{1}: Sample request received.'\
                .format(self.module_name,
                        self.method_name)
            )

            success = 'success'
            status = '200'
            message = 'Sample'
            data = {"sample":"value"}

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

        self.controller.log('{0}-{1}: Sample request returned: {2} '\
            .format(self.module_name,
                    self.method_name,
                    data)
        )

        return return_value


