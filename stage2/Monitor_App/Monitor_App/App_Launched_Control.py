from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App.Control import global_control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class App_Launched_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = global_control

    def app_launched(self, application=None, json_string=None):
        success = 'success'
        status = 200
        message = 'Monitor App detected an application launch.'
        data = {"application":application}

        try:
            self.__controller.log('{0}'.format(message))
            monitor_list = []
            monitored_apps = self.__controller.get_apps()
            for app in monitored_apps:
                monitor_list.append(app[0])
            if application.upper() not in monitor_list:
                message += ' Application not on watch list. Ignored.'
                self.__controller.log(
                    'Application {0} not on watch list. Ignored.'\
                    .format(application))
            else:
                self.__controller.log(
                    'Application {0} is on watch list.'.format(application))
                recipient = self.__controller.get_value('recipient')
                service = self.__controller.get_value('service')
                if recipient == [] or service == []:
                    raise ValueError('The recipient or service is not set. '+
                                     'It is not possible to post a notification.'
                                    )
                payload_data = {
                    "key":"1234-5678-9012-3456",
                    "message":"The application {0} has been launched"\
                        .format(application)+\
                        ". Remember: Safe sex is good sex!",
                    "sender":"Monitor_App",
                    "recipient":recipient,
                    "action":"none"
                }
                request_response = requests.post(
                    service,
                    data=json.dumps(payload_data)
                )
                self.__controller.log(
                    'Notification raised with data: '\
                    .format(payload_data))
                if request_response.status_code not in (200,201):
                    message += '. A warning was issued with the status code '+\
                               '{0}'.format(request_response.status_code)+\
                               '. Response data was: '+\
                               '{0}'.format(request_response.json())
                    success = 'warning'
                    self.__controller.log(message)
                else:
                    log_string = str(request_response.status_code) + ': ' + \
                                 str(request_response.json())
                    self.__controller.log(log_string)
        except requests.exceptions.ConnectionError as rce:
            message = 'Unable to connect to the notification service '+\
                      'to issue notification for {0}!'.format(application)
            status = 400
            success = 'warning'
            data = {"recipient":recipient or None, "service":service or None}
            self.__controller.log(message)
        except ValueError as ve:
            message = str(ve)
            status = 400
            success = 'warning'
            data = {"recipient":recipient or None, "service":service or None}
            self.__controller.log(message)
        except Exception as e:
            print(repr(e))
            self.__controller.log(repr(e))
            raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


global_app_launched_control = App_Launched_Control()
