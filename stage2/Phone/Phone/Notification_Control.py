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
        self.__controller = Control.Control_v1_00()

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
                if not key == 'NS1234-5678-9012-3456':
                    raise ValueError('Notification control key incorrect.')

                data = {"action":action,
                        "notification":text}
                now = datetime.datetime.now()
                tz = time.tzname[0]
                tzdst = time.tzname[1]

                self.__display_notification(
                    sender=sender,
                    date_string='{0} ({1}/{2})'.format(now, tz, tzdst),
                    notification=text,
                    action=action
                )

                self.__controller.persist_notification(
                    sender=sender,
                    date_string='{0} ({1}/{2})'.format(now, tz, tzdst),
                    notification=text,
                    action=action
                )

                response = self.__issue_bluetooth(
                    notification=text
                )
                if response != None and response.status_code != 200:
                    data['warnings'] = response.json()

            except requests.exceptions.ConnectionError as rce:
                # Connection error means we could not reach the Bluetooth
                # device. Ignore it but add a warning to the output as the
                # notification was still delivered.
                data['warnings'] = 'Bluetooth Error: device did not respond'
            except KeyError as ke:
                success = 'error'
                status = '400'
                message = 'Badly formed request!'
                continue_sentinel = False
            except ValueError as ve:
                success = 'error'
                status = '403'
                message = str(ve)
                continue_sentinel = False
            except Exception as e:
                success = 'error'
                status = '400'
                message = 'Badly formed request!'
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


#
# Version 1.00
# ----------------------------------------------------------------------------
class Notification_Control_v1_00(Notification_Control):
    def future(self):
        pass
