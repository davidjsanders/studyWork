from Monitor_App.v3_00_App_Launched_Control import v3_00_App_Launched_Control

from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App.Control import global_control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class v3_01_App_Launched_Control(v3_00_App_Launched_Control):

    def __init__(self):
        super(v3_01_App_Launched_Control, self).__init__()

    def app_launched(self, application=None, json_string=None):
        success = 'success'
        status = 200
        message = 'Monitor App detected an application launch.'
        data = {"application":application}

        try:
            self.controller.log('{0}'.format(message))

            recipient = self.controller.get_value('recipient')
            service = self.controller.get_value('service')

            monitored_apps = self.controller.get_app(application=application)
            if monitored_apps in ([], None, ''):
                raise ValueError('App {0} is not being monitored.'\
                    .format(application))

            self.controller.log(
                'Application {0} is on watch list.'.format(application)+\
                  ' Raising notification.'
            )

            message_to_send = self.controller.get_app_message()\
                .format(application)

            payload_data = {
                "key":"1234-5678-9012-3456",
                "message":"{0}".format(message_to_send),
                "sender":"Monitor_App",
                "recipient":recipient,
                "action":"none"
            }

            request_response = requests.post(
                service,
                data=json.dumps(payload_data)
            )

            self.controller.log(
                'Notification raised with data: '\
                .format(payload_data))

            if request_response.status_code not in (200,201):
                raise ValueError(
                    '. A warning was issued with the status code '+\
                    '{0}'.format(request_response.status_code)+\
                    '. Response data was: '+\
                    '{0}'.format(request_response.json())
                )

            log_string = str(request_response.status_code) + ': ' + \
                         str(request_response.json())
            self.controller.log(log_string)
        except requests.exceptions.ConnectionError as rce:
            message = 'Unable to connect to the notification service '+\
                      'to issue notification for {0}!'.format(application)
            data = {"recipient":recipient or None,\
                    "notification-service":service or None}
            success = "error"
            status = 400
            self.controller.log(message)
        except ValueError as ve:
            message = str(ve)
            success = "error"
            status = 404
            data = {"recipient":recipient or None,\
                    "notification-service":service or None}
            self.controller.log(message)
        except Exception as e:
            success = "error"
            data = {"recipient":recipient or None,\
                    "notification-service":service or None}
            status = 400
            message = repr(e)
            self.controller.log('Exception! {0}'.format(message))

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


