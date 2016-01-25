from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import Control, Pairing_Control
import datetime, time, json

#
# SuperClass.
# ----------------------------------------------------------------------------
class Broadcast_Control(object):
    __broadcast_filename = 'datavolume/broadcasted_output.txt'
    __display_filename = 'datavolume/display_output.txt'
    __controller = None

    def __init__(self):
        self.__controller = Control.Control_v1_00()


    def broadcast_message(self, devicename='Unknown', text=None, key=None):
        pair_control_object = Pairing_Control.Pairing_Control_v1_00()
        success = 'success'
        status = '200'
        message = 'Message has been broadcast.'
        data = {"device":devicename,
                "action":"broadcast",
                "message":text}

        pairing_key = pair_control_object.check_pairing(devicename)

        if pairing_key == []:
            success = 'error'
            status = '403'
            message = 'Device is not paired'
            pairing_key = None
        elif pairing_key != key:
            success = 'error'
            status = '403'
            message = 'Device pairing key is incorrect!'
            pairing_key = None
        elif text == '' or text == None:
            success = 'error'
            status = '403'
            message = 'Cannot broadcast an empty message'
            pairing_key = None
        else:
            try:
                now = datetime.datetime.now()
                tz = time.tzname[0]
                tzdst = time.tzname[1]

                f = open(self.__broadcast_filename,'a')
                f.write(('-'*80)+"\n")
                f.write('Broadcast from: {0}'.format(devicename)+"\n")
                f.write('Read aloud at: {0} ({1}/{2})'\
                    .format(now, tz, tzdst)+"\n")
                f.write('Message: {0}'.format(text)+"\n\n")
                f.close()

                f = open(self.__display_filename,'a')
                f.write(('-'*80)+"\n")
                f.write('Broadcast from: {0}'.format(devicename)+"\n")
                f.write('Shown on screen at: {0} ({1}/{2})'\
                    .format(now, tz, tzdst)+"\n")
                f.write('Message: {0}'.format(text)+"\n\n")
                f.close()
            except:
                raise

        return self.__controller.do_response(message=message,
                                   data=data,
                                   status=status,
                                   response=success)

#
# Version 1.00
# ----------------------------------------------------------------------------
class Broadcast_Control_v1_00(Broadcast_Control):
    def future(self):
        pass

