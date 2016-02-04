from flask_restful import Resource, Api, reqparse, abort
from flask import Response
#from Phone import Phone_Database
from Phone import Control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class Location_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_controller

    def location_request(
        self,
        json_string = None
    ):
        self.__controller.log('Location_Control:location_request:start',
                              screen=False)
        success = 'success'
        status = '200'
        message = 'Location.'
        data = None

        continue_sentinel = True
        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            if not key == '1234-5678-9012-3456':
                raise ValueError('Location control key incorrect.')
            x = float(self.__controller.get_value('x'))
            y = float(self.__controller.get_value('y'))
            data = {"x":x,"y":y}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
            self.__controller.log('Location_Control:location_request:{0}'\
                .format(str(ke)),
                screen=False
            )
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = str(ve)
            self.__controller.log('Location_Control:location_request:{0}'\
                .format(str(ve)),
                screen=False
            )
        except Exception as e:
            continue_sentinel = False
            self.__controller.log('Location_Control:location_request:{0}'\
                .format(repr(e)),
                screen=False
            )
            raise
            #return repr(e)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        self.__controller.log('Location_Control:location_request:end',
                              screen=False)
        self.__controller.log('',
                              screen=False)
        return return_value

location_control_object = Location_Control()
