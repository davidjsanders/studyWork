from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Phone import Control
import datetime, time, json, requests, os
from Phone.v3_00_Notification_Control import v3_00_Notification_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class v3_01_Notification_Control(v3_00_Notification_Control):

    def __init__(self):
        super(v3_01_Notification_Control, self).__init__()


#
# v3_01 Additions & Changes
#
    def incoming_notification(
        self,
        json_string=None
    ):
        success = 'success'
        status = '200'
        message = 'Notification received.'
        data = None
        now = datetime.datetime.now()
        tz = time.tzname[0]
        tzdst = time.tzname[1]

        date_string='{0} ({1}/{2})'.format(now, tz, tzdst)

        self.controller.log('Notification Control: Notification received.',
                              screen=False)

        try:
            json_data = json.loads(json_string)

            if json_string == None\
            or json_string == '':
                raise KeyError('No JSON Data provided!')

            self.controller.log('Notification Control: Parsing JSON data.',
                                  screen=False)
            text=json_data['message']
            key=json_data['key']
            sender=json_data['sender']
            action=json_data['action']

            self.controller.log('Notification Control: Validate key.',
                                  screen=False)
            if not key == 'NS1234-5678-9012-3456':
                raise ValueError('Notification control key incorrect.')

            self.controller.process_notification(
                sender=sender,
                date_string=date_string,
                notification=text,
                action=action
            )

            data = {"sender":sender,
                    "action":action,
                    "event-date":date_string,
                    "notification":text}

        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! {0}'.format(str(ke))
            self.controller.log('Incoming notification: Error {0}'\
                .format(str(ke)), screen=False)
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = str(ve)
            self.controller.log(
              'Notification Control: {0}'.format(message),
              screen=False
            )
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Exception: {0}'.format(repr(e))
            self.controller.log(
              'Incoming notification: Error {0}'.format(message),
              screen=False
            )

        self.controller.log('Notification Control: Processing completed.',
                              screen=False)

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


