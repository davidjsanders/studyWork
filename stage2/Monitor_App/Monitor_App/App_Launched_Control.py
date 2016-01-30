from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App import Control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class App_Launched_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.Control_v1_00()

    def app_launched(self, application=None, json_string=None):
        success = 'success'
        status = 200
        message = 'Monitor App has detected an application launch.'
        data = {"application":application}

        monitor_list = ['GRINDR','MANHUNT']
        if application.upper() not in monitor_list:
            message += ' Application not on watch list. Ignored.'
            return_value = self.__controller.do_response(message=message,
                                                         data=data,
                                                         status=status,
                                                         response=success)

            return return_value

        try:
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
                "recipient":recipient+'/notification',
                "action":"none"
            }
            request_response = requests.post(
                service+'/notification',
                data=json.dumps(payload_data)
            )
            if request_response.status_code not in (200,201):
                message += '. A warning was issued with the status code '+\
                           '{0}'.format(request_response.status_code)+\
                           '. Response data was: '+\
                           '{0}'.format(request_response.json())
                success = 'warning'
            else:
                log_string = str(request_response.status_code) + ': ' + \
                             str(request_response.json())
                self.__controller.print_error(log_string)
        except requests.exceptions.ConnectionError as rce:
            message = 'Unable to connect to the notification service.'
            status = 400
            success = 'warning'
            data = {"recipient":recipient or None, "service":service or None}
        except ValueError as ve:
            message = str(ve)
            status = 400
            success = 'warning'
            data = {"recipient":recipient or None, "service":service or None}
        except Exception as e:
            raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


#
# Version 1.00
# ----------------------------------------------------------------------------
class App_Launched_Control_v1_00(App_Launched_Control):
    def future(self):
        pass
