from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App.Control import global_control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class v3_00_App_Control(object):
    controller = None

    def __init__(self):
        self.controller = global_control

    def get_all(self):
        success = 'success'
        status = 200
        message = 'Monitor App list of monitored apps.'
        data = None

        try:
            monitored_apps = self.controller.get_apps()
            if monitored_apps in ([], None, ''):
                raise IndexError('No applications are being monitored.')

            monitored_app_list = []
            for app in monitored_apps:
                monitored_app_list.append(
                  {
                    "app":app[0].upper(),
                    "description":app[1]
                  }
                )

            data = {"apps":monitored_app_list}
        except IndexError as ie:
            message = str(ie)
            status = 404
            success = 'error'
            self.controller.log('{0}.'.format(message))
        except Exception as e:
            message = repr(e)
            status = 500
            success = 'error'
            self.controller.log('Unexpected Error: {0}.'.format(message))

        self.controller.log('Request to get all apps monitored.')

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def get(self, application=None):
        success = 'success'
        status = 200
        message = 'Monitor App application check.'
        data = None

        try:
            self.controller.log(
                'Check monitoring status of app {0}.'.format(application))
            monitor_list = self.controller.get_app(application)

            if monitor_list in (None, [], ''):
                raise ValueError('Application {0} is not being monitored.'\
                    .format(application))

            description = monitor_list[0][1]
            if description in (None, [], ''):
                description = 'no description provided'

            data = {"app":application.upper(), "description":description}
            self.controller.log('{0}'.format(message))
        except ValueError as ve:
            message = str(ve)
            status = 404
            success = 'error'
            self.controller.log('{0}.'.format(message))
        except Exception as e:
            message = repr(e)
            status = 500
            success = 'error'
            self.controller.log('Unexpected Error: {0}.'.format(message))

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def set(self, application=None, json_string=None):
        success = 'success'
        status = 200
        message = ''
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)

            key = json_data['key']
            description = json_data['description']

            if not key == '1234-5678-9012-3456':
                raise ValueError('App control key incorrect.')

            self.controller.log(
                'Request to monitor status of app {0} ({1}).'\
                .format(application, description))
            app_list = self.controller.set_app(application, description)

            if app_list in (None, [], ''):
                raise Exception('Monitor App application {0} not created!'\
                    .format(application))

            if description in (None, [], ''):
                description = 'no description provided'

            message = 'Application {0} ({1}) is now being monitored.'\
                .format(application, description)

            data = {"app":application.upper(), "description":description}
            self.controller.log('{0}'.format(message))
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! Missing {0}'.format(str(ke))
            self.controller.log('Key Error: {0}.'.format(message))
        except ValueError as ve:
            message = str(ve)
            status = 400
            success = 'warning'
            self.controller.log('{0}.'.format(message))
        except Exception as e:
            message = repr(e)
            status = 500
            success = 'error'
            self.controller.log('Unexpected Error: {0}.'.format(message))

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def delete(self, application=None, json_string=None):
        success = 'success'
        status = 200
        message = 'Monitor App application set.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('No JSON data provided')

            json_data = json.loads(json_string)

            key = json_data['key']

            if not key == '1234-5678-9012-3456':
                raise ValueError('App control key incorrect.')

            self.controller.log(
                'Request to stop monitoring app {0}.'.format(application))

            app_list = self.controller.get_app(application)
            if app_list in (None, [], ''):
                raise ValueError('Application {0} is not being monitored!'\
                    .format(application))

            app_list = self.controller.delete_app(application)

            message = 'Application {0} is no longer being monitored.'\
                .format(application.upper())
            data = None

            self.controller.log('{0}'.format(message))
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! Missing {0}'.format(str(ke))
            self.controller.log('Key Error: {0}.'.format(message))
        except ValueError as ve:
            message = str(ve)
            status = 404
            success = 'error'
            self.controller.log('{0}.'.format(message))
        except Exception as e:
            message = repr(e)
            status = 500
            success = 'error'
            self.controller.log('Unexpected Error: {0}.'.format(message))

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value



