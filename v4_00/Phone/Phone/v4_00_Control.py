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
from Phone.v3_01_Control import v3_01_Control

#
# SuperClass.
# ----------------------------------------------------------------------------
class v4_00_Control(v3_01_Control):

    def __init__(self):
        super(v3_01_Control, self).__init__()
        self.lock_device(False)

#
# v4_00 Context Check. Updated to use central context service
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
# v4_00 process_context. Use central context service.
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



