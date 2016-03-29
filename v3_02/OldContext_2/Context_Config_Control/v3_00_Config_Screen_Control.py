from flask_restful import Resource
from flask import Response, send_file
from Phone import Control
import json

class v3_00_Config_Screen_Control(object):
    controller = None

    def __init__(self):
        self.controller = Control.global_controller


    def get_screen(self):
        success = 'success'
        status = '200'
        message = 'Unlock device action.'
        data = None

        return_response = None

        try:
            output_device = '/Phone/{0}'\
                .format(self.controller.get_value('output_device'))
            return_response = send_file(output_device)
        except Exception as e:
            error_msg = 'An exception occurred: {0}'.format(repr(e))
            print(error_msg)
            self.controller.log(error_msg, screen=False)

        return return_response

