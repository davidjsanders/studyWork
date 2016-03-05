from flask_restful import Resource
from flask import Response
from Monitor_App import Control
import json, requests

class Config_Message_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_control


    def get_message(self, msg):
        success = 'success'
        status = '200'
        message = 'Monitor App message {0}: '.format(msg)
        data = None

        self.__controller.log('Request to get message {0}'\
                              .format(msg)
                             )
        msg_text = self.__controller.get_value(msg)
        if msg_text in ([], '', None):
            success = 'error'
            status = 404
            message = message + 'not found.'
            msg_text = None
        else:
            data = {'message':msg_text}
            self.__controller.log('Message for {0} is: {1}'\
                                  .format(msg, msg_text)
                                 )
            message = message + msg_text

        try:
            return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)
        except Exception as e:
            self.__controller.log('General exception: {0}'.format(repr(e)))
            raise

        return return_value


    def remove_message(self, msg=None, json_string=None):
        success = 'success'
        status = '200'
        message = 'Monitor App message {0}: '.format(msg)
        data = None

        self.__controller.log('Request to remove (or reset) message {0}'\
                              .format(msg)
                             )
        try:
            if msg in (None, '', []) \
            or json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']

            if not key == '1234-5678-9012-3456':
                raise ValueError('Logging key incorrect.')

            msg_text = self.__controller.get_value(msg)
            if msg_text in (None, '', []):
                success = 'error'
                status = 404
                message = message + 'not found.'
                msg_text = None
            else:
                self.__controller.clear_value(msg)
                default_message = self.__controller.get_value('default_'+msg)
                if not default_message in (None, '', []):
                    msg_text = default_message
                    self.__controller.set_value(msg, msg_text)
                else:
                    msg_text = None
                message = message + 'reset to {0}'.format(msg_text)
                data = {'message reset to':msg_text}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
            self.__controller.log('Key Error exception: {0}'.format(message))
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = str(ve)
            self.__controller.log('Value Error exception: {0}'.format(message))
        except Exception as e:
            self.__controller.log('General exception: {0}'.format(repr(e)))
            raise
            #return repr(e)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def set_message(self, msg=None, json_string=None):
        success = 'success'
        status = '200'
        message = 'Monitor App message {0}:'.format(msg)
        data = None

        try:
            if msg in (None, '', []) \
            or json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            msg_text = json_data['message-text']

            if not key == '1234-5678-9012-3456':
                raise ValueError('key incorrect.')

            self.__controller.log('Request to set {0} message to : {1}'\
                                  .format(msg, msg_text)
                                 )
            data = {'message':msg_text}
            self.__controller.set_value(msg, msg_text)
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! {0}'.format(ke)
            self.__controller.log('Key Error exception: {0}'.format(message))
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = str(ve)
            self.__controller.log('Value Error exception: {0}'.format(message))
        except Exception as e:
            self.__controller.log('General exception: {0}'.format(repr(e)))
            raise
            #return repr(e)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

logger_message_object = Config_Message_Control()

