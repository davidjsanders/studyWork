from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Location_Service.Control import global_control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class Check_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = global_control

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

            self.__controller.log('Location service request to check '+\
                                  '({0},{1})'.format(x, y))

            hotspots = self.__controller.get_hotspots_by_location(x, y)
            if hotspots != [] and type(hotspots) == list:
                data={"hotspot":True}
                data['hotspots'] = []
                hotspot_counter = 0
                for i, hotspot in enumerate(hotspots):
                    print(str(i))
                    hotspot_counter += 1
                    data['hotspots'].append(
                       {'location':hotspot[0],
                        'lower-x':hotspot[3],
                        'lower-y':hotspot[4],
                        'upper-x':hotspot[1],
                        'upper-y':hotspot[2],
                        'description':hotspot[5]}
                    )

                data['number'] = hotspot_counter
                data['x'] = x
                data['y'] = y
                self.__controller.log(
                    log_message='Location ({0},{1}) found in {2} hot spot.'\
                                .format(x, y, hotspot_counter))
            else:
                success='warning'
                message = 'No hotspots found.'
                data={"hotspot":False, "x":x, "y":y}
                self.__controller.log(
                    log_message='Location ({0},{1}) not in any hot spot.'\
                                .format(x, y))
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request. Missing {0}'.format(str(ke))
            self.__controller.log(
                log_message='{0}'\
                    .format(message))
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = str(ve)
            self.__controller.log(
                log_message='Location check error: {0}'\
                    .format(message))
        except Exception as e:
            success = 'error'
            status = '400'
            message = repr(e)
            self.__controller.log(
                log_message='Location service error: {0}'\
                    .format(message))
            raise

        return  self.__controller.do_response(message=message,
                                              data=data,
                                              status=status,
                                              response=success)

global_check_control = Check_Control()
