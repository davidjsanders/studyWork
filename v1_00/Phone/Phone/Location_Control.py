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

    def location_request(self):
        self.__controller.log('Location request received.',
                              screen=False)

        success = 'success'
        status = '200'
        message = 'Location'
        data = None

        try:
            x = float(self.__controller.get_value('x'))
            y = float(self.__controller.get_value('y'))
            data = {"x":x,"y":y}
        except KeyError as ke:
            success = 'error'
            status = '500'
            message = 'Key Error: {0}'.format(str(ke))
            self.__controller.log('Location request: Error {0}'\
                                      .format(message),
                                      screen=False
                                 )
        except ValueError as ve:
            success = 'error'
            status = '500'
            message = 'Value Error: {0}'.format(str(ve))
            self.__controller.log('Location request: Error {0}'\
                                      .format(message),
                                      screen=False
                                 )
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Exception: {0}'.format(repr(e))
            self.__controller.log('Location request: Error {0}'\
                                      .format(message),
                                      screen=False
                                 )

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        self.__controller.log('Location request returned {0}'.format(data),
                              screen=False)
        return return_value

location_control_object = Location_Control()

