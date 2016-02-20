from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App.Control import global_control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class State_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = global_control

    def get_state(self):
        success = 'success'
        status = '200'
        message = 'Monitor App state.'
        data = None

        self.__controller.log('{0} Status requested'.format(message))
        state_set = self.__controller.get_state()
        recipient_set = self.__controller.get_value('recipient')
        service_set = self.__controller.get_value('service')
        data = {"state":state_set,
                "recipient":recipient_set,
                "service":service_set
               }
        self.__controller.log('{0} Status reported as {1}'\
            .format(message, data))

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

        self.__controller.log('{0} Change to {1}'.format(message, state))

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
            self.__controller.log('{0} Changed to {1}'.format(message, state))
            if state.upper() == 'ON':
                # Extract values from JSON data
                recipient = json_data['recipient']
                service = json_data['notification-service']
                location_service = json_data['location-service']
                location_provider = json_data['location-provider']

                # Store values
                recipient_set = \
                    self.__controller.set_value('recipient',recipient)
                service_set = self.__controller.set_value('service',service)
                location_service_set = \
                    self.__controller.set_value('location-service',
                                                location_service)
                location_provider = \
                    self.__controller.set_value('location-provider',
                                                location_provider)
            else:
                recipient_set = self.__controller.clear_value('recipient')
                service_set = self.__controller.clear_value('service')
                location_service_set = \
                    self.__controller.clear_value('location-service')

            data = {"state":state_set,
                    "recipient":recipient_set,
                    "service":service_set,
                    "location-service":location_service_set
                   }
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request. Missing {0}'.format(str(ke))
            self.__controller.log(message)
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = str(ve)
            self.__controller.log(message)
        except Exception as e:
            success = 'error'
            status = '400'
            message = repr(e)
            self.__controller.log(message)
            raise

        return  self.__controller.do_response(message=message,
                                              data=data,
                                              status=status,
                                              response=success)

global_state_control = State_Control()
