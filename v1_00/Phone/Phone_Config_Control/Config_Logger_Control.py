from flask_restful import Resource
from flask import Response
from Phone import Control
import json, requests

class Config_Logger_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_controller


    def get_logger(self):
        success = 'success'
        status = '200'
        message = 'Central logging status.'

        self.__controller.log('Request to get central logger details.',
                              screen=False)
        logger = self.__controller.get_value('logger')
        if logger in ([], '', None):
            logger = None

        data = {'logger':logger}
        self.__controller.log('Central logger details: {0}'.format(data),
                              screen=False)

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

            self.__controller.log('Request to stop central logging.',
                                  screen=False)

            json_data = json.loads(json_string)

            key = json_data['key']
            self.__controller.log('Validating key.',
                                  screen=False)

            if not key == '1234-5678-9012-3456':
                raise ValueError('Logging key incorrect.')

            logger = self.__controller.get_value('logger')
            self.__controller.log('Validating logger',
                                  screen=False)

            if logger in (None, '', []):
                raise ValueError('The phone is not logging, '+\
                                 'so central logging cannot be switched off.')

            self.__controller.clear_value('logger')
            data = {'logger':None}
            self.__controller.log('Central logger details: {0}'.format(data),
                                  screen=False)

        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Config Logger, Key Error: {0}'.format(str(ke))
            self.__controller.log(message, screen=False)
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = 'Config Logger, Value Error: {0}'.format(str(ve))
            self.__controller.log(message, screen=False)
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Config Logger, Exception: {0}'.format(repr(e))
            self.__controller.log(message, screen=False)

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

            self.__controller.log('Request to start central logging.',
                                  screen=False)

            json_data = json.loads(json_string)

            self.__controller.log('Validating key.',
                                  screen=False)
            key = json_data['key']
            if not key == '1234-5678-9012-3456':
                raise ValueError('Logging key incorrect.')

            self.__controller.log('Validating logger details.',
                                  screen=False)
            logger = json_data['logger']

            self.__controller.log('Setting logger to: {0}'.format(logger),
                                  screen=False)

            self.__controller.set_value('logger', logger)
            data = {'logger':logger}
            self.__controller.log('Central logger details: {0}'.format(data),
                                  screen=False)
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Config Logger, Key Error: {0}'.format(str(ke))
            self.__controller.log(message, screen=False)
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = 'Config Logger, Value Error: {0}'.format(str(ve))
            self.__controller.log(message, screen=False)
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Config Logger, Exception: {0}'.format(repr(e))
            self.__controller.log(message, screen=False)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        self.__controller.log("Logging request for Phone. "+\
                              "Response: {0} - {1}. Message = {2}".\
                              format(status, data, message),
                              screen=False)

        return return_value

logger_control_object = Config_Logger_Control()

