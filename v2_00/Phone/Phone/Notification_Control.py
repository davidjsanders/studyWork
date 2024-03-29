from flask_restful import Resource, Api, reqparse, abort
from flask import Response
#from Phone import Phone_Database
from Phone import Control
import datetime, time, json, requests, os

#
# SuperClass.
# ----------------------------------------------------------------------------
class Notification_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_controller

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
                self.__controller.log(
                    '*** This is where the context check will happen ***',
                    screen=False
                )
                text=json_data['message']
                key=json_data['key']
                sender=json_data['sender']
                action=json_data['action']
                if not key == 'NS1234-5678-9012-3456':
                    raise ValueError('Notification control key incorrect.')

                lock_status = self.__controller.get_value('locked')
                self.__controller.log('Checking lock status. Value is {0}'\
                                      .format(lock_status),
                                      screen=False
                                     )

                data = {"action":action,
                        "notification":text}
                now = datetime.datetime.now()
                tz = time.tzname[0]
                tzdst = time.tzname[1]

                self.__controller.log(
                    'Persisting notification to primary storage.',
                    screen=False
                )

                self.__controller.persist_notification(
                    sender=sender,
                    date_string='{0} ({1}/{2})'.format(now, tz, tzdst),
                    notification=text,
                    action=action
                )

                if lock_status.upper() == 'UNLOCKED':
                    self.__controller.process_notification(
                        sender=sender,
                        date_string='{0} ({1}/{2})'.format(now, tz, tzdst),
                        notification=text,
                        action=action
                    )
#                    self.__controller.log(
#                        'Displaying notification on screen',
#                        screen=False
#                    )
#
#                    self.__controller.display_notification(
#                        sender=sender,
#                        date_string='{0} ({1}/{2})'.format(now, tz, tzdst),
#                        notification=text,
#                        action=action
#                    )
#
#                    self.__controller.log(
#                        'Incoming notification issued to Bluetooth listeners',
#                        screen=False
#                    )
#
#                    response = self.__controller.issue_bluetooth(
#                        notification=text
#                    )
#
#                    if response != None and response.status_code != 200:
#                        data['warnings'] = response.json()
                else:
                    self.__controller.log(
                        'Notification will not be displayed because '+\
                        'phone is locked.',
                        screen=False
                    )


            except requests.exceptions.ConnectionError as rce:
                # Connection error means we could not reach the Bluetooth
                # device. Ignore it but add a warning to the output as the
                # notification was still delivered.
                data['warnings'] = 'Bluetooth Error: device did not respond'
                self.__controller.log(
                    'Bluetooth device caused an error: {0}'\
                    .format(str(rce),
                    screen=False)
                )
            except KeyError as ke:
                success = 'error'
                status = '400'
                message = 'Badly formed request!'
                self.__controller.log(
                  'Handling incoming notification with bad key:{0}'\
                  .format(str(ke)),
                  screen=False
                )
            except ValueError as ve:
                success = 'error'
                status = '403'
                message = str(ve)
                self.__controller.log(
                  'Incoming notification caused an error:{0}'.format(str(ve)),
                  screen=False
                )
            except Exception as e:
                success = 'error'
                status = '400'
                message = 'Badly formed request!'
                self.__controller.log(
                  'Incoming notification caused exception :{0}'.format(repr(e)),
                  screen=False
                )
                raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def __issue_bluetooth(
        self,
        notification=None
    ):
        request_response = None

        try:
            bluetooth_device = self.__controller.get_bluetooth()
            if bluetooth_device != []\
            and bluetooth_device != None:
                bluetooth_key = self.__controller.get_value(bluetooth_device)
                phonename = self.__controller.get_value('phonename')
                if not (bluetooth_key == None or phonename == None):
                    payload_data = {
                                    "key":bluetooth_key,
                                    "message":notification
                                   }
                    request_response = requests.post(
                         bluetooth_device+'/broadcast/'+phonename,
                         data=json.dumps(payload_data)
                    )
            return request_response
        except requests.exceptions.ConnectionError as rce:
            raise requests.exceptions.ConnectionError(rce)
        except:
            raise

    def __display_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        try:
            self.__controller.log('')
            self.__controller.log('Notification received')
            self.__controller.log('-'*79)
            self.__controller.log('Notification from: {0}'.format(sender))
            self.__controller.log('Received at      : {0}'.format(date_string))
            self.__controller.log('Notification     : {0}'.format(notification))
            self.__controller.log('Action           : {0}'.format(action))
            self.__controller.log('')

            outputfile = self.__controller.get_value('output_device')
            f = open(outputfile,'a')
            f.write(('-'*80)+"\n")
            f.write('Notification from: {0}'.format(sender)+"\n")
            f.write('Received at      : {0}'.format(date_string)+"\n")
            f.write('Notification     : {0}'.format(notification)+"\n")
            f.write('Action           : {0}'.format(action)+"\n\n")
            f.close()
        except:
            raise


notification_control_object = Notification_Control()

