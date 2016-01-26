from flask_restful import Resource, Api, reqparse, abort
from flask import Response
#from Phone import Phone_Database
from Phone import Control
import datetime, time, json

#
# SuperClass.
# ----------------------------------------------------------------------------
class Notification_Control(object):
    __controller = None
    __output_devices = [
                        'datavolume/onscreen_notifications.txt'
                       ]

    def __init__(self):
        self.__controller = Control.Control_v1_00()

    def incoming_notification(
        self,
        text=None,
        key=None,
        sender=None,
        action=None
    ):
        success = 'success'
        status = '200'
        message = 'Notification received. Thank you.'
        data = {"action":action,
                "notification":text}

        if key == None\
        or text == None\
        or sender == None\
        or action == None:
            success = 'error'
            status = '400'
            message = 'Poorly formed notification!'
        elif not key == '1234-5678-9012-3456':
            success = 'error'
            status = '403'
            message = 'Notification control key does not match!'
        else:
            try:

                now = datetime.datetime.now()
                tz = time.tzname[0]
                tzdst = time.tzname[1]

                for outputfile in self.__output_devices:
                    print('Incoming Notification! Bing Bong!')
                    f = open(outputfile,'a')
                    f.write(('-'*80)+"\n")
                    f.write('Notification from: {0}'.format(sender)+"\n")
                    f.write('Received at      : {0} ({1}/{2})'\
                        .format(now, tz, tzdst)+"\n")
                    f.write('Notification     : {0}'.format(text)+"\n")
                    f.write('Action           : {0}'.format(action)+"\n\n")
                    f.close()

            except:
                raise

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


#
# Version 1.00
# ----------------------------------------------------------------------------
class Notification_Control_v1_00(Notification_Control):
    def future(self):
        pass
