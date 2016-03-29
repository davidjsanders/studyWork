from flask_restful import Resource, Api, reqparse, abort
from flask import Response
#from Phone import Phone_Database
from Phone import Control
import datetime, time, json, requests, os

#
# SuperClass.
# ----------------------------------------------------------------------------
class v3_00_Notification_Control(object):
    controller = None

    def __init__(self):
        self.controller = Control.global_controller

    def incoming_notification(
        self,
        json_string=None
    ):
        self.controller.log('Notification received.',
                              screen=False)
        success = 'success'
        status = '200'
        message = 'Notification received.'
        data = None


        if json_string == None\
        or json_string == '':
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
            self.controller.log(
                'Notification was not properly formed. There was no JSON.',
                screen=False)
        else:
            json_data = json.loads(json_string)
            continue_sentinel = True
            try:
                text=json_data['message']
                key=json_data['key']
                sender=json_data['sender']
                action=json_data['action']

                if not key == 'NS1234-5678-9012-3456':
                    raise ValueError('Notification control key incorrect.')

                data = {"sender":sender,
                        "action":action,
                        "notification":text}

                self.controller.log(
                    'Notification data: {0}'.format(data),
                    screen=False)

                now = datetime.datetime.now()
                tz = time.tzname[0]
                tzdst = time.tzname[1]

                self.controller.log(
                    'Sending display notification request.',
                    screen=False
                )

                self.display_notification(
                    sender=sender,
                    date_string='{0} ({1}/{2})'.format(now, tz, tzdst),
                    notification=text,
                    action=action
                )

                self.controller.log(
                    'Persisting notification to the database.',
                    screen=False
                )
                self.controller.persist_notification(
                    sender=sender,
                    date_string='{0} ({1}/{2})'.format(now, tz, tzdst),
                    notification=text,
                    action=action
                )

                self.controller.log(
                    'Issuing notification to bluetooth',
                    screen=False
                )
                response = self.issue_bluetooth(
                    notification=text
                )

                if response != None and response.status_code != 200:
                    data['bluetooth-warnings'] = response.json()

            except requests.exceptions.ConnectionError as rce:
                # Connection error means we could not reach the Bluetooth
                # device. Ignore it but add a warning to the output as the
                # notification was still delivered.
                data['bluetooth-warnings'] = \
                    'Bluetooth Error: device did not respond. {0}'\
                        .format(str(rce))
                self.controller.log(data['bluetooth-warnings'],
                                      screen=False)
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
                  'Incoming notification: {0}'.format(message),
                  screen=False
                )
            except Exception as e:
                success = 'error'
                status = '400'
                message = 'Exception: {0}'.format(repr(e))
                self.controller.log(
                  'Incoming notification: Error {0}'.format(message),
                  screen=False
                )

        self.controller.log('Notification processed.',
                              screen=False)
        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def issue_bluetooth(
        self,
        notification=None
    ):
        request_response = None

        try:
            bluetooth_device = self.controller.get_bluetooth()
            if bluetooth_device != []\
            and bluetooth_device != None:
                bluetooth_key = self.controller.get_value(bluetooth_device)
                phonename = self.controller.get_value('phonename')
                if not (bluetooth_key == None or phonename == None):
                    payload_data = {"key":bluetooth_key,
                                    "message":notification}
                    request_response = requests.post(
                         bluetooth_device+'/broadcast/'+phonename,
                         data=json.dumps(payload_data)
                    )
            return request_response
        except requests.exceptions.ConnectionError as rce:
            raise requests.exceptions.ConnectionError(rce)
        except:
            raise

    def display_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        try:
            self.controller.log('-'*77,
                                screen=True)
            self.controller.log('Notification received',
                                screen=True)
            self.controller.log('-'*77,
                                screen=True)
            self.controller.log('Notification from: {0}'.format(sender),
                                screen=True)
            self.controller.log('Received at      : {0}'.format(date_string),
                                screen=True)
            self.controller.log('Notification     : {0}'.format(notification),
                                screen=True)
            self.controller.log('Action           : {0}'.format(action),
                                screen=True)
            self.controller.log('-'*77,
                                screen=True)

            outputfile = self.controller.get_value('output_device')
            f = open(outputfile,'a')
            f.write(('-'*80)+"\n")
            f.write('Notification from: {0}'.format(sender)+"\n")
            f.write('Received at      : {0}'.format(date_string)+"\n")
            f.write('Notification     : {0}'.format(notification)+"\n")
            f.write('Action           : {0}'.format(action)+"\n\n")
            f.close()
        except:
            raise

