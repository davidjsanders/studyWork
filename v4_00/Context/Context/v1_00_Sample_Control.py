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

    def sample_request(self):
        try:
            self.controller.log('Sample request received.')

            success = 'success'
            status = '200'
            message = 'Sample'
            data = {"sample":"value"}

        except Exception as e:
            success = 'error'
            status = '500'
            message = 'An error occurred.'
            error_text = 'v1_00_Sample_Control.sample_request_all: '+\
                'Exception {0}'.format(repr(e))
            data = {"exception":error_text}
            print(error_text)

        return_value = self.controller.do_response(message=message,
                                                   data=data,
                                                   status=status,
                                                   response=success)

        self.controller.log('Sample request returned {0}'.format(data))

        return return_value


