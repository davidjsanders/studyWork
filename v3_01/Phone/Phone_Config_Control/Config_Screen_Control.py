from flask_restful import Resource
from flask import Response, send_file
from Phone import Control
import json

class Config_Screen_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_controller


    def get_screen(self):
        success = 'success'
        status = '200'
        message = 'Unlock device action.'
        data = None

        return_response = None

        try:
            output_device = '/Phone/{0}'\
                .format(self.__controller.get_value('output_device'))
            return_response = send_file(output_device)
        except Exception as e:
            error_msg = 'An exception occurred: {0}'.format(repr(e))
            print(error_msg)
            self.__controller.log(error_msg, screen=False)

        return return_response


screen_control_object = Config_Screen_Control()


