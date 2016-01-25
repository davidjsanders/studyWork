from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import Pairing_Database
from Bluetooth import Control
import datetime, time, json

#
# SuperClass.
# ----------------------------------------------------------------------------
class Pairing_Control(object):
    __pairing_db = None
    __config_database = 'datavolume/config.db'
    __display_filename = 'datavolume/display_output.txt'
    __controller = None


    def __init__(self):
        self.__pairing_db = Pairing_Database.Pairing_Database()
        self.__controller = Control.Control_v1_00()

    def check_pairing(self, devicename):
        return self.__pairing_db.check_pairing(devicename)

    def pair_info(self, devicename):
        success = 'success'
        status = '200'
        message = 'Device is paired.'
        pairing = self.check_pairing(devicename)

        if pairing == []:
            success = 'error'
            status = '404'
            message = 'Device is not paired'
            pairing = None

        data = {"device":devicename,
                "key":pairing}

        return self.__controller.do_response(message=message,
                                data=data,
                                status=status,
                                response=success)

    def pair_device(self, devicename):
        success = 'success'
        status = '200'
        message = 'Device successfully paired.'
        existing_key = self.check_pairing(devicename) or None

        if existing_key != None:
            success = 'error'
            status = '409'
            message = 'The device is already paired.'
            data = {"device":devicename,
                    "key":existing_key}
        else:
            data = {"device":devicename,
                    "key":self.__pairing_db.pair_device(devicename)}
        return self.__controller.do_response(message=message,
                                data=data,
                                status=status,
                                response=success)

    def pair_unpair(self, devicename):
        if not self.check_pairing(devicename):
            return self.__controller.do_response(status="404",
                                    response='error',
                                    message="{0} is not paired."\
                                        .format(devicename))
        if self.__pairing_db.remove_pairing(devicename):
            return self.__controller.do_response(message="{0} un-paired.".format(devicename))


#
# Version 1.00
# ----------------------------------------------------------------------------
class Pairing_Control_v1_00(Pairing_Control):
    def future(self):
        pass

