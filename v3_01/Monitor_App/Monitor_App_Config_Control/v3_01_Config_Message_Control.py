#
# v3_01 is the FIRST version
#
from flask_restful import Resource
from flask import Response
from Monitor_App import Control
import json, requests

class v3_01_Config_Message_Control(object):
    controller = None

    def __init__(self):
        self.controller = Control.global_control


    def get_app_message(self):
        return self.get_message('app_msg')


    def get_location_message(self):
        return self.get_message('location_msg')


    def set_app_message(self, json_string):
        return self.set_message('app_msg', json_string)


    def set_location_message(self, json_string):
        return self.set_message('location_msg', json_string)


    def get_message(self, msg_type='app_msg'):
        success = 'success'
        status = '200'
        message = 'Get Monitor App app message'
        data = None

        self.controller.log('Request to get {0} message.'.format(msg_type))

        if msg_type.upper() == 'APP_MSG':
            msg_text = self.controller.get_app_message()
        else:
            msg_text = self.controller.get_location_message()

        data={"text":msg_text}

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        self.controller.log('Monitor App {0} message is set to {1}.'\
            .format(msg_type, msg_text))

        return return_value


    def set_message(self, msg_type='app_msg', json_string=None):
        success = 'success'
        status = '200'
        message = 'Set Monitor App app message'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('No JSON data provided!')

            json_data = json.loads(json_string)
            key = json_data['key']
            msg_text = json_data['text']

            if not key == '1234-5678-9012-3456':
                raise ValueError('control key incorrect.')

            self.controller.log('Setting {0} message to : {1}'\
                                      .format(msg_type, msg_text)
                                 )

            data = {'text':msg_text}

            if msg_type.upper() == 'LOCATION_MSG':
                self.controller.set_location_message(msg_text)
            else:
                self.controller.set_app_message(msg_text)

            self.controller.log('Message {0} set to {1}'\
                                      .format(msg_type, msg_text)
                                 )
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! {0}'.format(ke)
            self.controller.log('Key Error exception: {0}'.format(message))
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = str(ve)
            self.controller.log('Value Error exception: {0}'.format(message))
        except Exception as e:
            self.controller.log('General exception: {0}'.format(repr(e)))
            raise
            #return repr(e)

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


