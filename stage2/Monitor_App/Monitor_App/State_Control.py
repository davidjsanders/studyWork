from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App import Control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class State_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.Control_v1_00()

    def get_state(self):
        success = 'success'
        status = '200'
        message = 'Monitor App state.'
        data = None

        state_set = self.__controller.get_state()
        recipient_set = self.__controller.get_value('recipient')
        service_set = self.__controller.get_value('service')
        data = {"state":state_set,
                "recipient":recipient_set,
                "service":service_set
               }

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def set_state(self, state=None, json_string=None):
        success = 'success'
        status = '200'
        message = 'State change request.'
        data = None

        try:
            if state == None\
            or state == ''\
            or json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']

            if not key == '1234-5678-9012-3456':
                raise ValueError('Monitor App key incorrect.')

            state_set = self.__controller.set_state(state)
            if state.upper() == 'ON':
                recipient = json_data['recipient']
                service = json_data['service']
                recipient_set = \
                    self.__controller.set_value('recipient',recipient)
                service_set = self.__controller.set_value('service',service)
            else:
                recipient_set = self.__controller.clear_value('recipient')
                service_set = self.__controller.clear_value('service')

            data = {"state":state_set,
                    "recipient":recipient_set,
                    "service":service_set
                   }
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request. Missing {0}'.format(str(ke))
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = str(ve)
        except Exception as e:
            success = 'error'
            status = '400'
            message = repr(e)
            raise

        return  self.__controller.do_response(message=message,
                                              data=data,
                                              status=status,
                                              response=success)

#
# Version 1.00
# ----------------------------------------------------------------------------
class State_Control_v1_00(State_Control):
    def future(self):
        pass
