# Import base library modules - From Bluetooth symbolic link to /base_lib
import base_lib
from base_lib.Responder import Responder
from base_lib.Config_Logger import Config_Logger
from base_lib.Logger import Logger
from base_lib.Environment import Environment
from base_lib.KVStore import KVStore

from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Context.Context_Database import Context_Database

import datetime, time, json, os, redis, requests
from textwrap import wrap

#
# SuperClass.
# ----------------------------------------------------------------------------
class v3_00_Control(object):
    log_file = None
    Context_db = None
    redis = {'host':'localhost', 'port':6379, 'db':0}

    server_name=None
    port_number=0

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
                             sender='Context-{1}'\
                                 .format(server_name, port_number))
        self.logger.writelog('Log written')
        #self.log = self.logger.writelog
        self.db_logger = self.logger.db_logger


        # General startup
        self.server_name = server_name
        self.port_number = port_number

        self.Context_db = Context_Database(self,
                                         self.server_name,
                                         self.port_number)

        self.log('Context {0}:{1} Started'\
                 .format(server_name, port_number))

        self.log('Setting environment variables to {0}'\
            .format(self.environment))
        self.set_value('server_name', server_name)
        self.set_value('port_number', port_number)
        self.set_value('ip_addr', host_ip)
        self.set_value('version', version)
        self.set_value('Contextname', '{0}_{1}'\
            .format(server_name, port_number))
        self.set_value('output_device', 
                       'datavolume/{0}_{1}-notifications.txt'\
                           .format(server_name, port_number))
        self.set_value('x','0')
        self.set_value('y','0')
        self.log('Stored environment variables')


    def persist_notification(
        self,
        sender=None,
        date_string=None,
        notification=None,
        action=None
    ):
        self.Context_db.save_notification(
            sender,
            date_string,
            notification,
            action
        )


    def get_bluetooth(self):
        return self.Context_db.get_bluetooth_device()


    def set_bluetooth(self, devicename=None):
        return self.Context_db.set_bluetooth_device(devicename)


    def write_screen(self, output_line=None):
        if output_line == None:
            return
        redis_instance = redis.StrictRedis(**self.redis)
        return redis_instance.publish(
            'output_screen',
            '{0}\n'.format(output_line)
            )


    def log(self,
            log_message=None,
            screen=False,
            log_to_central=True
    ):
        self.logger.writelog(log_message, log_to_central)
        if screen:
            now = str(datetime.datetime.now())
            self.write_screen(now+":"+log_message+"\n")


