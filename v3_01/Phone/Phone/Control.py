# Import base library modules - From Bluetooth symbolic link to /base_lib
import base_lib
from base_lib.Responder import Responder
from base_lib.Config_Logger import Config_Logger
from base_lib.Logger import Logger
from base_lib.Environment import Environment
from base_lib.KVStore import KVStore

from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Phone.Phone_Database import Phone_Database

import datetime, time, json, os, redis, requests
from textwrap import wrap

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(object):
    __log_file = None
    __phone_db = None
    __redis = {'host':'localhost', 'port':6379, 'db':0}

    __server_name=None
    __port_number=0

    config_logger = None

    def __init__(self):
        # Setup environment
        self.environment = Environment()
        port_number = self.environment['port_number']
        server_name = self.environment['server_name']
        host_ip = self.environment['ip_addr']
        version = self.environment['version']
        pre_filename = 'datavolume/{0}-{1}'\
                       .format(server_name, port_number)

        # Setup Config for Logger
        # self.config_logger = Config_Logger(self)

        # Setup responder
        self.responder = Responder()
        self.do_response = self.responder.do

        # Setup KV Store
        self.kvstore = KVStore(pre_filename+'-config.db')
        self.get_value = self.kvstore.get_key
        self.set_value = self.kvstore.set_key
        self.clear_value = self.kvstore.clear_key

        # Setup Logger
        self.logger = Logger(controller=self,
                             filename=pre_filename+'-log.txt',
                             sender='Phone-{1}'\
                                 .format(server_name, port_number))
        self.logger.writelog('Log written')
        #self.log = self.logger.writelog
        self.db_logger = self.logger.db_logger


        # General startup
        self.__server_name = server_name
        self.__port_number = port_number

        self.__phone_db = Phone_Database(self,
                                         self.__server_name,
                                         self.__port_number)

        self.log('Phone {0}:{1} Started'\
                 .format(server_name, port_number))

        self.log('Setting environment variables to {0}'\
            .format(self.environment))
        self.set_value('server_name', server_name)
        self.set_value('port_number', port_number)
        self.set_value('ip_addr', host_ip)
        self.set_value('version', version)
        self.set_value('phonename', '{0}_{1}'\
            .format(server_name, port_number))
        self.set_value('output_device', 
                       'datavolume/{0}_{1}-notifications.txt'\
                           .format(server_name, port_number))

        self.log('Output device = {0}'.format(self.get_value('output_device')),
                 screen=False
                )

        self.set_value('x','0')
        self.set_value('y','0')
        self.log('Stored environment variables')

#
# v3_00 Logic
#

    def persist_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        self.__phone_db.save_notification(
            sender,
            date_string,
            notification,
            action
        )


    def get_bluetooth(self):
        return self.__phone_db.get_bluetooth_device()


    def set_bluetooth(self, devicename=None):
        return self.__phone_db.set_bluetooth_device(devicename)


    def write_screen(self, output_line=None):
        if output_line == None:
            return
        redis_instance = redis.StrictRedis(**self.__redis)
        return redis_instance.publish(
            'output_screen',
            '{0}\n'.format(output_line)
            )


    def log(self,
            log_message=None,
            screen=True,
            log_to_central=True
    ):
        self.logger.writelog(log_message, log_to_central)
        if screen:
            self.write_screen(log_message+"\n")

#
# v3_01 Additions & Changes
#

    def handle_unlock(self):
        print('Unlock activated.')


    def process_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        try:
            self.persist_notification(
                sender=sender,
                date_string=date_string,
                notification=notification,
                action=action
            )

            # get states and values
            self.log('Process Notification: Getting states and values.',
                     screen=False)
            lock_status = self.get_value('locked')
            if lock_status in (None, [], ''):
                lock_status = 'unlocked'    # Default to unlocked
            if lock_status.upper() == 'LOCKED':
                self.log('Process Notification: Stopping - Phone is locked. '+\
                         'Notification will be persisted.',
                         screen=False)
                return


            bluetooth = self.get_bluetooth()
            output_device = self.get_value('output_device')

            # Log states and values
            self.log('Process Notification: Lock = {0}.'.format(lock_status),
                     screen=False)
            self.log('Process Notification: Bluetooth = {0}.'\
                         .format(bluetooth),
                     screen=False)
            self.log('Process Notification: Output_Device = {0}.'\
                         .format(output_device),
                     screen=False)


            self.log('Process Notification: Displaying notification',
                     screen=False)

            self.display_notification(
                sender=sender,
                date_string=date_string,
                notification=notification,
                action=action,
                output_device=output_device
            )

            self.log('Process Notification: Checking for Bluetooth.',
                     screen=False)

            if not bluetooth in ('',[],None):
                self.issue_bluetooth(
                    notification=notification,
                    bluetooth=bluetooth
                )

            self.log('Process Notification: Updating notification to read.',
                     screen=False)

            self.__phone_db.update_notification(
                sender=sender,
                date_string=date_string,
                notification=notification,
                action=action,
            )

        except Exception as e:
            raise

        print('process notification')

#
# v3_01: Moved from Notification_Control to Control
#
    def display_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None,
        output_device='unknown.txt'
    ):
        try:
            self.log('-'*77)
            self.log('Notification received')
            self.log('-'*77)
            self.log('Notification from: {0}'.format(sender))
            self.log('Received at      : {0}'.format(date_string))
            self.log('Notification     : {0}'.format(notification))
            self.log('Action           : {0}'.format(action))
            self.log('-'*77)

            f = open(output_device,'a')
            f.write(('-'*80)+"\n")
            f.write('Notification from: {0}'.format(sender)+"\n")
            f.write('Received at      : {0}'.format(date_string)+"\n")
            f.write('Notification     : {0}'.format(notification)+"\n")
            f.write('Action           : {0}'.format(action)+"\n\n")
            f.close()
        except:
            raise


    def issue_bluetooth(
        self,
        notification=None,
        bluetooth=None
    ):
        self.log('Issue Bluetooth: Start',
                 screen=False)

        request_response = None
        if bluetooth == None:
            self.log('Issue Bluetooth: Bluetooth is None.',
                     screen=False)
            return

        try:
            bluetooth_device = self.get_bluetooth()
            if not bluetooth_device in ([], None, ''):
                bluetooth_key = self.get_value(bluetooth_device)
                phonename = self.get_value('phonename')
                if not (bluetooth_key == None or phonename == None):
                    payload_data = {"key":bluetooth_key,
                                    "message":notification}
                    self.log('Issue Bluetooth: Posting request to '+\
                             '{0} with payload {1}'\
                                 .format(bluetooth_device+\
                                            '/broadcast/'+phonename,
                                         payload_data),
                             screen=False)
                    request_response = requests.post(
                         bluetooth_device+'/broadcast/'+phonename,
                         data=json.dumps(payload_data),
                         timeout=15
                    )
            return request_response
        except requests.exceptions.ConnectionError as rce:
            self.log(
                'Bluetooth caused an exception: {0}'.format(rce),
                screen=False
            )
        except Exception as e:
            self.log(
                'Bluetooth caused an exception: {0}'.format(repr(e)),
                screen=False
            )

        self.log('Issue Bluetooth: End',
                 screen=False)


global_controller = Control()

