from flask_restful import Resource
from flask import Response
from Phone import Control
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

            self.__controller.set_value('x', str(x))
            self.__controller.set_value('y', str(y))

            data = {"x":x, "y":y}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = str(ve)
        except IndexError as ie:
            success = 'error'
            status = '403'
            message = str(ie)
        except Exception as e:
            raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def get_loc(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Get location details.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']

            if not key == '1234-5678-9012-3456':
                raise ValueError('Control key incorrect.')

            x = float(self.__controller.get_value('x'))
            y = float(self.__controller.get_value('y'))

            data = {"x":x, "y":y}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = str(ve)
        except Exception as e:
            raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

config_location_control_object = Config_Location_Control()

