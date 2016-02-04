from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App.Control import global_control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class App_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = global_control

    def get_all(self):
        success = 'success'
        status = 200
        message = 'Monitor App list of monitored apps.'
        data = None

        try:
            monitored_apps = self.__controller.get_apps()
            data = {"apps":monitored_apps}

        except Exception as e:
            message = repr(e)
            status = 500
            success = 'error'
            self.__controller.log('Unexpected Error: {0}.'.format(message))
            raise

        self.__controller.log('Request to get all apps monitored.')

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

        return "all"

    def get(self, application=None):
        success = 'success'
        status = 200
        message = 'Monitor App application check.'
        data = None

        try:

            self.__controller.log(
                'Check monitoring status of app {0}.'.format(application))
            monitor_list = self.__controller.get_app(application)
            if monitor_list in (None, [], ''):
                success = 'error'
                status = 404
                message = 'Application {0} not found.'\
                    .format(application)
                self.__controller.log('{0}'.format(message))
            else:
                description = monitor_list[0][1]
                if description in (None, [], ''):
                    description = 'no description provided'
                message += ' {0} ({1}) is being monitored.'\
                    .format(application, description)
                self.__controller.log('{0}'.format(message))

        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! Missing {0}'.format(str(ke))
            self.__controller.log('Key Error: {0}.'.format(message))
        except ValueError as ve:
            message = str(ve)
            status = 400
            success = 'warning'
            self.__controller.log('Value Error: {0}.'.format(message))
        except Exception as e:
            message = repr(e)
            status = 500
            success = 'error'
            self.__controller.log('Unexpected Error: {0}.'.format(message))
            raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def set(self, application=None, json_string=None):
        success = 'success'
        status = 200
        message = 'Monitor App application set.'
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

            self.__controller.log(
                'Request to monitor status of app {0} ({1}).'\
                .format(application, description))
            app_list = self.__controller.set_app(application, description)
            if app_list in (None, [], ''):
                success = 'error'
                status = 404
                message = 'Monitor App application {0} not created!'\
                    .format(application)
                self.__controller.log('{0}'.format(message))
            else:
                if description in (None, [], ''):
                    description = 'no description provided'
                message += ' {0} ({1}) is now being monitored.'\
                    .format(application, description)
                data = {"app":application, "description":description}
                self.__controller.log('{0}'.format(message))
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! Missing {0}'.format(str(ke))
            self.__controller.log('Key Error: {0}.'.format(message))
        except ValueError as ve:
            message = str(ve)
            status = 400
            success = 'warning'
            self.__controller.log('Value Error: {0}.'.format(message))
        except Exception as e:
            message = repr(e)
            status = 500
            success = 'error'
            self.__controller.log('Unexpected Error: {0}.'.format(message))
            raise

        return_value = self.__controller.do_response(message=message,
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

            self.__controller.log(
                'Request to stop monitoring app {0}.'.format(application))
            app_list = self.__controller.get_app(application)
            if app_list in (None, [], ''):
                success = 'error'
                status = 404
                message = 'Application {0} is not being monitored!'\
                    .format(application)
                self.__controller.log('{0}'.format(message))
            else:
                app_list = self.__controller.delete_app(application)
                if app_list:
                    message += ' {0} is no longer being monitored.'\
                        .format(application)
                self.__controller.log('{0}'.format(message))
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! Missing {0}'.format(str(ke))
            self.__controller.log('Key Error: {0}.'.format(message))
        except ValueError as ve:
            message = str(ve)
            status = 400
            success = 'warning'
            self.__controller.log('Value Error: {0}.'.format(message))
        except Exception as e:
            message = repr(e)
            status = 500
            success = 'error'
            self.__controller.log('Unexpected Error: {0}.'.format(message))
            raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


global_app_control = App_Control()
