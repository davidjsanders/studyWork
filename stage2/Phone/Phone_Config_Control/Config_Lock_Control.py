from flask_restful import Resource
from flask import Response
from Phone import Control
import json

class Config_Lock_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_controller


    def is_locked(self):
        success = 'success'
        status = '200'
        message = 'Device lock status.'
        data = None

        self.__controller.log('Request to check if phone is locked.',
                              screen=False)
        current_state = self.__controller.get_value('locked')
        data = {'locked':current_state}

        self.__controller.log('Request returned: {0}'.format(data),
                              screen=False)
        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def lock_request(self):
        success = 'success'
        status = '200'
        message = 'Lock device action.'
        data = None

        self.__controller.log('Locking phone.', screen=False)
        lock_state = self.__controller.set_value('locked','locked')
        data = {'locked':lock_state}
        self.__controller.log('Phone locked.', screen=False)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def unlock_request(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Unlock device action.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            self.__controller.log('Request to unlock phone.', screen=False)

            json_data = json.loads(json_string)
            key = json_data['key']
            if not key == '1234-5678-9012-3456':
                raise ValueError('Unlock key incorrect.')

            lock_state = self.__controller.set_value('locked','unlocked')
            data = {'locked':lock_state}
            self.__controller.log('Phone unlocked.', screen=False)
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Unlock, Key Error: {0}'.format(str(ke))
            self.__controller.log(message, screen=False)
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = 'Unlock, Value Error: {0}'.format(str(ve))
            self.__controller.log(message, screen=False)
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Unlock, Exception: {0}'.format(repr(e))
            self.__controller.log(message, screen=False)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

lock_control_object = Config_Lock_Control()


