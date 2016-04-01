from flask_restful import Resource
from flask import Response
from Module import Control

class v1_00_Config_Sample_Control(object):
    controller = None

    def __init__(self):
        self.controller = Control.global_controller


    def not_implemented(self, route=None):
        self.method_name = 'not_implemented'

        success = 'error'
        status = '500'
        message = 'Not Implemented.'
        data = None

        return_value = self.controller.do_response(message=message,
                                                   data=data,
                                                   status=status,
                                                   response=success)

        self.controller.log('{0}-{1}: Route {2} not implemented'\
            .format(self.module_name,
                    self.method_name,
                    route)
        )

        return return_value


    def sample_request(self):
        try:
            self.controller.log('Config sample request received.')

            success = 'success'
            status = '200'
            message = 'Sample'
            data = {"config-sample":"config-value"}

        except Exception as e:
            success = 'error'
            status = '500'
            message = 'An error occurred.'
            error_text = 'v1_00_Config_Sample_Control.sample_request'+\
                ': Exception {0}'.format(repr(e))
            data = {"exception":error_text}
            print(error_text)

        return_value = self.controller.do_response(message=message,
                                                   data=data,
                                                   status=status,
                                                   response=success)

        self.controller.log('Sample request returned {0}'.format(data))

        return return_value


