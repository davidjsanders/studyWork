from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service.Control import global_control
import datetime, time, json, requests, redis, copy

#
# SuperClass.
# ----------------------------------------------------------------------------
class v3_00_Notification_Receiver(object):
    controller = None

    def __init__(self):
        self.controller = global_control

    def incoming_notification(
        self,
        json_string=None
    ):
        success = 'success'
        status = '201'
        message = 'Notification received. Thank you.'
        data = None

        self.controller.log('Notification received.')

        if json_string == None\
        or json_string == '':
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
        else:
            json_data = json.loads(json_string)
            continue_sentinel = True
            try:
                data = copy.deepcopy(json_data)
                text=json_data['message']
                key=json_data['key']
                sender=json_data['sender']
                action=json_data['action']
                recipient=json_data['recipient']
                if not key == '1234-5678-9012-3456':
                    status = '403'
                    raise ValueError('Notification control key incorrect.')

                if 'http://' not in recipient:
                    status = '400'
                    raise ValueError('Recipient must be a valid URL '+\
                                     'beginning with http://'
                    )

                del data['key']
                self.controller.log('Notification from {0} for {1}'\
                                     .format(sender,recipient))

                self.controller.log('Notification is {0} with action: {1}'\
                                     .format(text, action))

            except KeyError as ke:
                success = 'error'
                status = '400'
                message = 'Badly formed request Missing {0}!'.format(ke)
                self.controller.log(message)
                continue_sentinel = False
            except ValueError as ve:
                success = 'error'
                message = str(ve)
                self.controller.log(message)
                continue_sentinel = False
            except Exception as e:
                success = 'error'
                status = '500'
                message = 'Exception: {0}'.format(repr(e))
                self.controller.log(message)
                continue_sentinel = False

            if continue_sentinel:
                try:
                    now = datetime.datetime.now()
                    tz = time.tzname[0]
                    tzdst = time.tzname[1]

                    # Dispatch notification to redis pub/sub to enable fast
                    # collection of notifications and then let another thread
                    # take time to process.

                    self.controller.log(
                        'Notification Receiver is queuing Notification '+\
                        'with data: '+\
                        '{0}-{1}-{2}-{3}-{4}'\
                            .format(
                                sender,
                                recipient,
                                text,
                                action,
                                str(now)+'('+tz+'/'+tzdst+')'
                            )
                    )
                    self.controller.queue_notification(
                        sender,
                        recipient,
                        text,
                        action,
                        str(now)+'('+tz+'/'+tzdst+')'
                    )
                except:
                    success = 'error'
                    status = '500'
                    message = 'Exception: {0}'.format(repr(e))
                    self.controller.log(message)

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

