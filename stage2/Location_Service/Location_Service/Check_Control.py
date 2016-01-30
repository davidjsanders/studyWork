from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Location_Service import Control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class Check_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.Control_v1_00()

    def check(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Location Service, check location results.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']

            if not key == '1234-5678-9012-3456':
                raise ValueError('Location Service key incorrect.')

            x = float(json_data['x'])
            y = float(json_data['y'])

            hotspots = self.__controller.get_hotspots()
            if hotspots != [] and type(hotspots) == list:
                for hotspot in hotspots:
                    upperX = hotspot[0]
                    upperY = hotspot[1]
                    lowerX = hotspot[2]
                    lowerY = hotspot[3]
                    hotspot_desc = hotspot[4]
                    if (x >= lowerX and x <= upperX) \
                    and (y >= lowerY and y <= upperY):
                        data={"hotspot":True}
                    else:
                        data={"hotspot":False}
                    data['x'] = x
                    data['y'] = y
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
class Check_Control_v1_00(Check_Control):
    def future(self):
        pass
