from flask_restful import Resource, Api, reqparse, abort
from flask import Response
#from Notification_Service import Notification_Service_Database
from Notification_Service import Control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class Lock_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.Control_v1_00()


    def is_locked(self):
        success = 'success'
        status = '200'
        message = 'Device lock status.'
        data = {'locked':True}

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def lock_request(self):
        success = 'success'
        status = '200'
        message = 'Lock device action.'
        data = {'locked':True}

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

        continue_sentinel = True
        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            if not key == '1234-5678-9012-3456':
                raise ValueError('Unlock key incorrect.')
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
            continue_sentinel = False
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = str(ve)
            continue_sentinel = False
        except Exception as e:
            raise
            #return repr(e)

        if continue_sentinel:
            data = {'locked':False}

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


#
# Version 1.00
# ----------------------------------------------------------------------------
class Lock_Control_v1_00(Lock_Control):
    def future(self):
        pass
