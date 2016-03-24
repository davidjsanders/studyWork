from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service.Control import global_control
import datetime, time, json, requests

#
# SuperClass.
# ----------------------------------------------------------------------------
class v3_00_Notification_Push_Control(object):
    controller = None
#    redis = {'host':'localhost', 'port':6379, 'db':0}

    def __init__(self):
        self.controller = global_control

    def push_notifications(
        self,
        json_string=None
    ):
        success = 'success'
        status = '200'
        message = 'Notification push request.'
        data = None

        self.controller.log('Push Request received.')
        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            recipient = json_data['recipient']

            if not key == '1234-5678-9012-3456':
                status = '403'
                raise ValueError('Push notification control key incorrect.')

            if 'http://' not in recipient:
                status = '400'
                raise ValueError('Recipient must be a valid URL '+\
                                 'beginning with http://'
                )

            self.controller.log('Request received from {0}.'\
                .format(recipient))

            notification_list = []

            self.controller.log('Fetching persisted notifications for {0}.'\
                .format(recipient))
            notification_list = self.controller.fetch_notifications(recipient)

            self.controller.log('Found {0} notifications.'\
                .format(len(notification_list)))

            if not notification_list == None:
                counter = 0
                for notification in notification_list:
                    counter += 1
                    self.controller.log('Requesting push of #{0}.'\
                        .format(counter))
                    self.controller.queue_notification(
                            notification[1],
                            notification[2],
                            notification[3],
                            notification[4],
                            notification[5]
                    )
                    self.controller.log('Clearing notification from db.')
                    self.controller.clear_notification(notification[0])

            if counter == 0:
                status = '404'
                success = 'error'

            data={
                    "recipient":recipient,
                    "notification-count":"{0}".format(counter),
                 }

            self.controller.log('Final status: {0}.'\
                .format(status))

        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! {0}'.format(str(ke))
            self.controller.log(message)
        except ValueError as ve:
            success = 'error'
            message = str(ve)
            self.controller.log(message)
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Exception: {0}'.format(repr(e))
            self.controller.log(message)

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

