from flask_restful import Resource
from flask import Response
from Phone import Control
import json
from Phone_Config_Control.v3_00_Config_Lock_Control \
    import v3_00_Config_Lock_Control

class v3_01_Config_Lock_Control(v3_00_Config_Lock_Control):

    def __init__(self):
        super(v3_01_Config_Lock_Control, self).__init__()


    def is_locked(self):
        success = 'success'
        status = '200'
        message = 'Device lock status.'
        data = None

        self.controller.log('Config Lock Control: Checking phone lock state.',
                              screen=False)

        current_state = self.controller.get_lock_status()
        data = {'locked':current_state}

        self.controller.log('Config Lock Control: Phone is {0}'\
                                  .format(current_state),
                              screen=True)

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def lock_request(self):
        success = 'success'
        status = '200'
        message = 'Lock device action.'
        data = None

        self.controller.log('Config Lock Control: Locking phone.',
                              screen=False)

        lock_state = self.controller.lock_device(True)
        data = {'locked':lock_state}

        self.controller.log('Config Lock Control: Phone locked.',
                              screen=True)

        return_value = self.controller.do_response(message=message,
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

            self.controller.log('Config Lock Control: unlock phone.',
                                  screen=False)

            json_data = json.loads(json_string)
            key = json_data['key']
            if not key == '1234-5678-9012-3456':
                raise ValueError('Unlock key incorrect.')

            lock_state = self.controller.lock_device(False)
            data = {'locked':lock_state}

            self.controller.log('Config Lock Control: Phone unlocked.',
                                  screen=True)
            self.controller.handle_unlock()
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Unlock, Key Error: {0}'.format(str(ke))
            self.controller.log(message, screen=False)
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = 'Unlock, Value Error: {0}'.format(str(ve))
            self.controller.log(message, screen=False)
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Unlock, Exception: {0}'.format(repr(e))
            self.controller.log(message, screen=False)

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

