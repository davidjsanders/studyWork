from flask_restful import Resource
from flask import Response
from Phone import Control
from Phone.Location_Control import location_control_object
#import Phone.Location_Control
import json, requests

class Config_Location_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_controller


    def set_loc(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Set location details.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']

            if not key == '1234-5678-9012-3456':
                raise IndexError('Control key incorrect.')

            x = float(json_data['x'])
            y = float(json_data['y'])

            self.__controller.log('Request to set location to {0},{1}'\
                                  .format(x,y), screen=False)

            self.__controller.set_value('x', str(x))
            self.__controller.set_value('y', str(y))

            data = {"x":x, "y":y}
            self.__controller.log('Location changed.', screen=False)
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Set location, Key Error: {0}'.format(str(ke))
            self.__controller.log(message, screen=False)
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = 'Set location, Value Error: {0}'.format(str(ve))
            self.__controller.log(message, screen=False)
        except IndexError as ie:
            success = 'error'
            status = '403'
            message = 'Set location, Index Error: {0}'.format(str(ie))
            self.__controller.log(message, screen=False)
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Set location, Exception: {0}'.format(repr(e))
            self.__controller.log(message, screen=False)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

config_location_control_object = Config_Location_Control()

