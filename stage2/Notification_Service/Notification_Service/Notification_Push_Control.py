from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service.Control import global_control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class Notification_Push_Control(object):
    __controller = None
    __redis = {'host':'localhost', 'port':6379, 'db':0}

    def __init__(self):
        self.__controller = global_control

    def push_notifications(
        self,
        json_string=None
    ):
        success = 'success'
        status = '200'
        message = 'Notification push request.'
        data = None

        self.__controller.log('Push Request received.')
        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            recipient = json_data['recipient']
            self.__controller.log('Request received from {0}.'\
                .format(recipient))
            if not key == '1234-5678-9012-3456':
                raise ValueError('Push notification control key incorrect.')

            notification_list = []
            self.__controller.log('Fetching persisted notifications for {0}.'\
                .format(recipient))
            notification_list = self.__controller.fetch_notifications(recipient)
            self.__controller.log('Found {0} notifications.'\
                .format(len(notification_list)))

            if not notification_list == None:
                counter = 0
                for notification in notification_list:
                    counter += 1
                    self.__controller.log('Requesting push of #{0}.'\
                        .format(counter))
                    self.__controller.queue_notification(
                            notification[1],
                            notification[2],
                            notification[3],
                            notification[4],
                            notification[5]
                    )
                    self.__controller.log('Clearing notifications from db.')
                    self.__controller.clear_notification(notification[0])

            data={
                    "status":"{0} notification(s) will be dispatched."\
                        .format(counter if counter != 0 else 'No')
                 }
            self.__controller.log('Final status: {0}.'\
                .format(data['status']))

        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
            self.__controller.log(message)
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = str(ve)
            self.__controller.log(message)
        except Exception as e:
            self.__controller.log(message)
            raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


global_notification_push_control = Notification_Push_Control()
