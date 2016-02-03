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

        self.__controller.log(log_message='PAIR INFO START: for "{0}"'\
            .format(devicename))
        if pairing == []:
            success = 'error'
            status = '404'
            message = 'Device is not paired'
            pairing = None
            self.__controller.log(log_message='PAIR INFO ERROR: {0}'\
                .format(message))

        data = {"device":devicename,
                "key":pairing}

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        self.__controller.log(log_message='PAIR INFO FINISH: for "{0}" ({1})'\
            .format(devicename, success))

        return return_value

    def pair_device(self, devicename):
        success = 'success'
        status = '200'
        message = 'Device successfully paired.'
        existing_key = self.check_pairing(devicename) or None

        self.__controller.log(log_message='PAIR DEVICE START: with "{0}"'\
            .format(devicename))

        data = {"device":devicename,
                "key":self.__pairing_db.pair_device(devicename)}

        return_value = self.__controller.do_response(message=message,
                                                   data=data,
                                                   status=status,
                                                   response=success)

        self.__controller.log(
             log_message='PAIR DEVICE FINISH: with "{0}" ({1} {2})'\
                .format(devicename, success, status)
        )

        return return_value

    def pair_unpair(self, devicename):
        self.__controller.log(log_message='UNPAIR DEVICE START: with "{0}"'\
            .format(devicename))

        if not self.check_pairing(devicename):
            self.__controller.log(
                log_message='UNPAIR DEVICE ERROR: {0} is not paired'\
                    .format(devicename))
            self.__controller.log(
                 log_message='UNPAIR DEVICE FINISH: with "{0}" ({1} {2})'\
                    .format(devicename, 'error', '404')
            )
            return self.__controller.do_response(status="404",
                                    response='error',
                                    message="{0} is not paired."\
                                        .format(devicename))

        if self.__pairing_db.remove_pairing(devicename):
            self.__controller.log(
                 log_message='UNPAIR DEVICE FINISH: with "{0}" ({1} {2})'\
                    .format(devicename, 'success', '200')
            )
            return self.__controller.do_response(
                message="{0} un-paired.".format(devicename))


    def get_output_devices(self, devicename=None):
        if devicename == None:
            return []

        return self.__pairing_db.get_output_devices(devicename)


    def remove_output_device(self, devicename=None, output_item=None):
        if devicename == None or output_item == None:
            return False
        if output_item == 'Default audio device':
            raise KeyError('Cannot remove default audio device.')

        valid_output_item = self.__pairing_db.get_output_device(
             devicename,
             output_item
            )

        if valid_output_item == [] or valid_output_item == None:
            raise KeyError('Output item {0} does not exist for device {1}'\
                           .format(output_item, devicename))

        return self.__pairing_db.remove_output_device(devicename, output_item)


    def add_output_device(self,
                          devicename=None,
                          output_item=None,
                          file_name=None):
        if devicename == None or output_item == None or file_name == None:
            return False
        if output_item == 'Default audio device':
            raise KeyError('Cannot add the default audio device.')

        return self.__pairing_db.add_output_device(devicename,
                                                   output_item,
                                                   file_name)


#
# Version 1.00
# ----------------------------------------------------------------------------
class Pairing_Control_v1_00(Pairing_Control):
    def future(self):
        pass

