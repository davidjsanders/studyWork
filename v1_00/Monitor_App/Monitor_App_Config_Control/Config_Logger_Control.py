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

        self.__controller.log('Central logger configured to {0}'\
            .format(logger)
        )
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
                raise ValueError('The Monitor App is not logging, '+\
                                 'so central logging cannot be switched off.')

            self.__controller.clear_value('logger')
            self.__controller.log('Central logger configured to null')
            data = {'logger':None}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! {0}'.format(str(ke))
            self.__controller.log('Key Error: {0}'.format(message))
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = str(ve)
            self.__controller.log('Value Error: {0}'.format(message))
        except Exception as e:
            success = 'error'
            status = '500'
            message = repr(e)
            self.__controller.log('Exception: {0}'.format(message))

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
            self.__controller.log('Central logger configured to {0}'\
                .format(logger)
            )
            data = {'logger':logger}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! {0}'.format(ke)
            self.__controller.log('Key Error: {0}'.format(message))
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = str(ve)
            self.__controller.log('Value Error: {0}'.format(message))
        except Exception as e:
            success = 'error'
            status = '500'
            message = repr(e)
            self.__controller.log('Exception: {0}'.format(message))

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        self.__controller.log("Logging request for Monitor App. "+\
                              "Response: {0} - {1}. Message = {2}".\
                              format(status, data, message))

        return return_value

logger_control_object = Config_Logger_Control()

