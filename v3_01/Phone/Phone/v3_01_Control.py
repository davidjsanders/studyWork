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
from Phone.v3_00_Control import v3_00_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class v3_01_Control(v3_00_Control):

    def __init__(self):
        super(v3_01_Control, self).__init__()
        self.lock_device(False)

#
# v3_01 Handle Unlock. Added to catch unlock requests and process any persisted
# notifications.
#

    def handle_unlock(self):
        self.log('Control - Unlocked: Process persisted '+\
                 'notifications.',
                 screen=False)
        notifications_persisted = self.phone_db.get_notifications()

        self.log('Control - Unlocked: Process {0} notifications.'\
                     .format(len(notifications_persisted)),
                 screen=False)

        for note in notifications_persisted:
            self.log('Control - Unlocked: '+\
                     'Processing notification received at {0}'\
                         .format(note[1]))
            self.process_context(
                sender=note[0],
                date_string=note[1],
                notification=note[2],
                action=note[3]
            )


#
# v3_01 Process Notification. Moved to Control so available from everywhere.
#
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

            self.process_context(
                sender=sender,
                date_string=date_string,
                notification=notification,
                action=action
            )

        except Exception as e:
            raise

        print('process notification')


#
# v3_01 Context Check. New in v3_01. Checks the context of the device.
#
    def local_context_check(self,
                            kvstore=None,
                            devicename=None
    ):
        return_context = True  # Default to an allowed context
        context_message = None

        try:
            # 1. Check lock status
            lock_status = self.get_lock_status()
            if lock_status.upper() == 'LOCKED':
                context_message = 'Not allowed. The phone is locked.'
                raise ValueError(context_message)

            context_message = 'Context check is good.'

            # 2. Check message severity

            # 3. Check isolation state
              # 3.1 Presence indicator - available, busy, dnd, etc.

            # 4. Check where / when / why / how / who

            self.log('Context check passed. {0}'.format(context_message),
                     screen=False)
        except ValueError as ve:
            return_context = False
            context_message = str(ve)
            self.log('Context check failed. {0}'.format(context_message),
                     screen=False)
        except Exception as e:
            # Fail to safe
            return_context = False
            context_message = 'Failed because of exception: {0}'\
                                  .format(repr(e))
            self.log('Context check failed. {0}'.format(context_message),
                     screen=False)

        return return_context, context_message


#
# v3_01 process_context. Private method that is called by process_notification
# and displays / processes notifications only if the context check is ok.
#
    def process_context(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        try:
            # get states and values
            self.log('Process Notification: Getting states and values.',
                     screen=False)

            context_ok, context_message = \
                self.local_context_check(
                    kvstore=self.kvstore,
                    devicename=self.get_value('phonename')
                )

            if not context_ok:
                self.log('Process Notification: Context issued '+\
                          'stop because >> {0} '.format(context_message)+\
                         'Notification will be persisted.',
                         screen=False)
                return

            bluetooth = self.get_bluetooth()
            output_device = self.get_value('output_device')

            # Log states and values
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
                action=action
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

            self.phone_db.update_notification(
                sender=sender,
                date_string=date_string,
                notification=notification,
                action=action,
            )
        except Exception as e:
            raise


#
# v3_01 Get Lock Status. New in v3_01. Checks whether the device is locked or
# unlocked.
#
    def get_lock_status(self):
        self.log('Get Lock Status.')

        lock_status = self.get_value('{0}-{1}-lock-state'\
                                         .format(self.server_name,
                                                 self.port_number)
        )

        if lock_status in ([], None, ''):
            lock_status = 'unlocked'    # Default to unlocked

        self.log('Get Lock Status returned {0}.'.format(lock_status))
        return lock_status


#
# v3_01 Lock Device. New in v3_01. Locks or unlocks the device.
#
    def lock_device(self, lock=True):
        if type(lock) is not bool:
            lock_state = 'locked'
        elif lock:
            lock_state='locked'
        else:
            lock_state='unlocked'

        self.set_value('{0}-{1}-lock-state'\
                           .format(self.server_name,
                                   self.port_number),
                       lock_state)

        return lock_state


#
# v3_01: Change to log to include file output within the log method.
#

    def log(self,
            log_message=None,
            screen=False,
            log_to_central=True
    ):
        self.logger.writelog(log_message, log_to_central)
        if screen:
            now = str(datetime.datetime.now())
            self.write_screen(now+": "+log_message+"\n")

            output_device = self.get_value('output_device')
            if output_device not in ('', None, []):
                try:
                    f = open(output_device,'a')
                    f.write(now+": "+log_message+"\n")
                except Exception as e:
                    error_msg = 'Log raised exception: {0}'.format(repr(e))
                    print(error_msg)
                    self.log(error_msg, screen=False, log_to_central=True)
                finally:
                    f.close()


#
# v3_01: Moved from Notification_Control to Control. Change to remove direct
# file I/O from the method and include as part of the logger.
#
    def display_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        try:
            self.log('-'*77, screen=True)
            self.log('Notification received', screen=True)
            self.log('-'*77, screen=True)
            self.log('Notification from: {0}'.format(sender), screen=True)
            self.log('Received at      : {0}'.format(date_string), screen=True)
            self.log('Notification     : {0}'.format(notification), screen=True)
            self.log('Action           : {0}'.format(action), screen=True)
            self.log('-'*77, screen=True)
        except Exception as e:
            error_msg = 'Display Notification. Exception: {0}'.format(repr(e))
            print(error_msg)
            self.log(error_msg, screen=False, log_to_central=True)


#
# v3_01: Moved from Notification_Control to Control. Changes are general tidy 
# up.
#
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


