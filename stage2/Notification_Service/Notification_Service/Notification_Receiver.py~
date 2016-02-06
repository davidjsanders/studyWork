from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service.Control import global_control
import datetime, time, json, requests
import redis

#
# SuperClass.
# ----------------------------------------------------------------------------
class Notification_Receiver(object):
    __controller = None

    def __init__(self):
        self.__controller = global_control

    def incoming_notification(
        self,
        json_string=None
    ):
        success = 'success'
        status = '201'
        message = 'Notification received. Thank you.'
        data = None


        if json_string == None\
        or json_string == '':
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
        else:
            json_data = json.loads(json_string)
            continue_sentinel = True
            try:
                text=json_data['message']
                key=json_data['key']
                sender=json_data['sender']
                action=json_data['action']
                recipient=json_data['recipient']
                if not key == '1234-5678-9012-3456':
                    raise ValueError('Notification control key incorrect.')
            except KeyError as ke:
                success = 'error'
                status = '400'
                message = 'Badly formed request Missing {0}!'.format(ke)
                self.__controller.log(message)
                continue_sentinel = False
            except ValueError as ve:
                success = 'error'
                status = '403'
                message = str(ve)
                self.__controller.log(message)
                continue_sentinel = False
            except Exception as e:
                self.__controller.log('Unexpected exception: {0}'\
                    .format(repr(e)))
                raise

            if continue_sentinel:
                data = {"action":action,
                        "notification":text}
                try:
                    now = datetime.datetime.now()
                    tz = time.tzname[0]
                    tzdst = time.tzname[1]

                    # Dispatch notification to redis pub/sub to enable fast
                    # collection of notifications and then let another thread
                    # take time to process.

                    self.__controller.queue_notification(
                        sender,
                        recipient,
                        text,
                        action,
                        str(now)+'('+tz+'/'+tzdst+')'
                    )
                    self.__controller.log('Queued {0}---{1}---{2}---{3}---{4}'\
                        .format(
                            sender,
                            recipient,
                            text,
                            action,
                            str(now)+'('+tz+'/'+tzdst+')'
                        )
                    )
                except:
                    raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


global_notification_receiver_control = Notification_Receiver()
