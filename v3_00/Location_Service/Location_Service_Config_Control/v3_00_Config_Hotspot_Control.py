from flask_restful import Resource
from flask import Response
from Location_Service.Control \
    import global_control as global_control
import json, requests

class v3_00_Config_Hotspot_Control(object):
    controller = global_control

    def __init__(self):
        pass


    def get_all(self):
        success = 'success'
        status = '200'
        message = 'Location Service, fetch all hotspots.'
        data = None

        try:
            self.controller.log('Location service request to show all '+\
                                  'hotspots')

            hotspots = self.controller.get_hotspots()
            data={"hotspots":hotspots}
            self.controller.log(
                log_message='Location Service returned the following '+\
                    'hotspots: {0}'.format(hotspots))
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request. Missing {0}'.format(str(ke))
            self.controller.log(
                log_message='{0}'\
                    .format(message))
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = str(ve)
            self.controller.log(
                log_message='Config hotspot error: {0}'\
                    .format(message))
        except Exception as e:
            success = 'error'
            status = '400'
            message = repr(e)
            self.controller.log(
                log_message='Config hotspot error: {0}'\
                    .format(message))

        return  self.controller.do_response(message=message,
                                              data=data,
                                              status=status,
                                              response=success)



    def get(self, location=None):
        success = 'success'
        status = '200'
        message = 'Location Service, fetch hotspot.'
        data = None

        try:
            self.controller.log(
                 log_message='Request to get hotspot "{0}"'.format(location))

            hotspots = self.controller.get_hotspot(location)
            if hotspots != None and hotspots != []:
                data={"hotspot":location,
                  "upper-x":hotspots[0][1],
                  "upper-y":hotspots[0][2],
                  "lower-x":hotspots[0][3],
                  "lower-y":hotspots[0][4],
                  "description":hotspots[0][5]
                 }
            else:
                raise ValueError('Hotspot {0} does not exist.'.format(location))
            self.controller.log(
                log_message='Location Service returned the following '+\
                    'information for hotspot {0}: {1}'.format(location, data))
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request. Missing {0}'.format(str(ke))
            self.controller.log(
                log_message='{0}'\
                    .format(message))
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = str(ve)
            self.controller.log(
                log_message='Config hotspot error: {0}'\
                    .format(message))
        except Exception as e:
            success = 'error'
            status = '400'
            message = repr(e)
            self.controller.log(
                log_message='Config hotspot error: {0}'\
                    .format(message))

        return  self.controller.do_response(message=message,
                                              data=data,
                                              status=status,
                                              response=success)



    def set(self, location=None, json_string=None):
        success = 'success'
        status = '200'
        message = 'Location service, set hotspot information.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            upperX = json_data['upper-x']
            upperY = json_data['upper-y']
            lowerX = json_data['lower-x']
            lowerY = json_data['lower-y']
            description = json_data['description']

            if not key == '1234-5678-9012-3456':
                raise IndexError('Location service key incorrect.')

            self.controller.log(
                log_message=
                    'Request to add hotspot "{0}" at ({1},{2})-({3},{4})'\
                         .format(location, lowerX, lowerY, upperX, upperY)+\
                    ' as "{0}"'.format(description))

            self.controller.save_hotspot(location=location,
                                           lowerX=lowerX,
                                           lowerY=lowerY,
                                           upperX=upperX,
                                           upperY=upperY,
                                           desc=description)

            data = {"hotspot":location,
                    "upper-x":upperX,
                    "upper-y":upperY,
                    "lower-x":lowerX,
                    "lower-y":lowerY,
                    "description":description}
            self.controller.log(
                log_message=
                    'Added hotspot "{0}" at ({3},{4})-({1},{2})'\
                         .format(location, lowerX, lowerY, upperX, upperY)+\
                    ' as "{0}"'.format(description))
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'A key is missing: '+str(ke)
            self.controller.log(
                log_message='Hotspot config error: {0}'\
                    .format(message))
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = str(ve)
            self.controller.log(
                log_message='Hotspot config error: {0}'\
                    .format(message))
        except IndexError as ie:
            success = 'error'
            status = '403'
            message = str(ie)
            self.controller.log(
                log_message='Hotspot config error: {0}'\
                    .format(message))
        except Exception as e:
            success = 'error'
            status = '400'
            message = repr(e)
            self.controller.log(
                log_message='Hotspot config error: {0}'\
                    .format(repr(e)))

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def delete(self, location=None, json_string=None):
        success = 'success'
        status = '200'
        message = 'Location service, delete hotspot information.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']

            if not key == '1234-5678-9012-3456':
                raise IndexError('Location service key incorrect.')

            self.controller.log(
                log_message=
                    'Request to remove hotspot "{0}"'\
                         .format(location))

            hotspots = self.controller.get_hotspot(location)
            if hotspots == None or hotspots == []:
                raise ValueError('Hotspot {0} does not exist.'.format(location))

            self.controller.delete_hotspot(location)

            data = {"hotspot":None}
            self.controller.log(
                log_message=
                    'Deleted hotspot "{0}".'\
                         .format(location))
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'A key is missing: '+str(ke)
            self.controller.log(
                log_message='Hotspot config error: {0}'\
                    .format(message))
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = str(ve)
            self.controller.log(
                log_message='Hotspot config error: {0}'\
                    .format(message))
        except IndexError as ie:
            success = 'error'
            status = '403'
            message = str(ie)
            self.controller.log(
                log_message='Hotspot config error: {0}'\
                    .format(message))
        except Exception as e:
            success = 'error'
            status = '400'
            message = repr(e)
            self.controller.log(
                log_message='Hotspot config error: {0}'\
                    .format(repr(e)))

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

