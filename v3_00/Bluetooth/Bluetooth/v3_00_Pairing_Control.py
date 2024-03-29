from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import Pairing_Database
from Bluetooth.Control import global_control
import datetime, time, json

#
# SuperClass.
# ----------------------------------------------------------------------------
class v3_00_Pairing_Control(object):
    pairing_db = None
    config_database = 'datavolume/config.db'
    display_filename = 'datavolume/display_output.txt'
    controller = global_control


    def __init__(self):
#        self.pairing_db = Pairing_Database.Pairing_Database()
        controller = global_control
        self.pairing_db = self.controller.get_pairing_db()

    def check_pairing(self, devicename):
        return self.pairing_db.check_pairing(devicename)

    def pair_info(self, devicename):
        success = 'success'
        status = '200'
        message = 'Device is paired.'
        pairing = self.check_pairing(devicename)

        self.controller.log('Pairing status request received for "{0}"'\
            .format(devicename))
        if pairing == []:
            success = 'error'
            status = '404'
            message = 'Device is not paired'
            pairing = None
            self.controller.log('A pairing error occurred: {0}'\
                .format(message))

        data = {"device":devicename,
                "key":pairing}

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        self.controller.log('Device "{0}" pairing request complete ({1})'\
            .format(devicename, success))

        return return_value

    def pair_device(self, devicename):
        success = 'success'
        status = '200'
        message = 'Device successfully paired.'
        existing_key = self.check_pairing(devicename) or None

        self.controller.log(log_message='Pair request from "{0}"'\
            .format(devicename))

        data = {"device":devicename,
                "key":self.pairing_db.pair_device(devicename)}

        return_value = self.controller.do_response(message=message,
                                                   data=data,
                                                   status=status,
                                                   response=success)

        self.controller.log(
             log_message='Paired with "{0}" ({1} {2})'\
                .format(devicename, success, status)
        )

        return return_value

    def pair_unpair(self, devicename):
        self.controller.log(log_message='Un-pair request received form "{0}"'\
            .format(devicename))

        if not self.check_pairing(devicename):
            self.controller.log(
                log_message='Un-pair error: {0} is not paired'\
                    .format(devicename))
            self.controller.log(
                 log_message='Un-pair error "{0}" ({1} {2})'\
                    .format(devicename, 'error', '404')
            )
            return self.controller.do_response(status="404",
                                    response='error',
                                    message="{0} is not paired."\
                                        .format(devicename))

        if self.pairing_db.remove_pairing(devicename):
            self.controller.log(
                 log_message='Device "{0}" un-paired. ({1} {2})'\
                    .format(devicename, 'success', '200')
            )
            return self.controller.do_response(
                message="{0} un-paired.".format(devicename))


    def get_output_devices(self, devicename=None):
        if devicename == None:
            return []

        return self.pairing_db.get_output_devices(devicename)


    def remove_output_device(self, devicename=None, output_item=None):
        if devicename == None or output_item == None:
            return False
        if output_item == 'Default audio device':
            raise KeyError('Cannot remove default audio device.')

        valid_output_item = self.pairing_db.get_output_device(
             devicename,
             output_item
            )

        if valid_output_item == [] or valid_output_item == None:
            raise ValueError('Output item {0} does not exist for device {1}'\
                           .format(output_item, devicename))

        return self.pairing_db.remove_output_device(devicename, output_item)


    def add_output_device(self,
                          devicename=None,
                          output_item=None,
                          file_name=None):
        if devicename == None or output_item == None or file_name == None:
            return False
        if output_item == 'Default audio device':
            raise KeyError('Cannot add the default audio device.')

        return self.pairing_db.add_output_device(devicename,
                                                   output_item,
                                                   file_name)


