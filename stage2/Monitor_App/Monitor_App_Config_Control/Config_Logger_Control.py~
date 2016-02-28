from flask_restful import Resource
from flask import Response
from Monitor_App import Control
import json, requests

class Config_Logger_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_control


    def get_logger(self):
        success = 'success'
        status = '200'
        message = 'Central logging status.'

        logger = self.__controller.get_value('logger')
        if logger in ([], '', None):
            logger = None

        data = {'logger':logger}
        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def remove_logger(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Central logging status.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            logger = self.__controller.get_value('logger')

            if not key == '1234-5678-9012-3456':
                raise ValueError('Logging key incorrect.')

            if logger in (None, '', []):
                raise ValueError('The phone is not logging, '+\
                                 'so central logging cannot be switched off.')

            self.__controller.clear_value('logger')
            data = {'logger':None}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = str(ve)
        except Exception as e:
            raise
            #return repr(e)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def set_logger(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Central logging status.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            logger = json_data['logger']

            if not key == '1234-5678-9012-3456':
                raise ValueError('Logging key incorrect.')

            self.__controller.set_value('logger', logger)
            data = {'logger':logger}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! {0}'.format(ke)
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = str(ve)
        except Exception as e:
            raise
            #return repr(e)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

logger_control_object = Config_Logger_Control()

