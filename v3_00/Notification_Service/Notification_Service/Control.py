# Import base library modules - From Bluetooth symbolic link to /base_lib
import base_lib
from base_lib.Responder import Responder
from base_lib.Config_Logger import Config_Logger
from base_lib.Logger import Logger
from base_lib.Environment import Environment
from base_lib.KVStore import KVStore

from Notification_Service.Notification_Service_Database \
    import Notification_Service_Database

import datetime, time, json, redis, os, requests
from textwrap import wrap

class Control(object):
    __log_file = None
    __Notification_Service_db = None
#    __redis = {'host':'localhost', 'port':6379, 'db':0}
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
        self.logger = Logger(filename=pre_filename+'-log.txt',
                             sender='{0}-{1}'\
                                 .format(server_name, port_number))
        self.logger.writelog('Log written')
        self.log = self.logger.writelog
        self.db_logger = self.logger.db_logger


        # General startup
        self.__server_name = server_name
        self.__port_number = port_number

        self.__Notification_Service_db = Notification_Service_Database(
            port_number=port_number,
            server_name=server_name
        )

        self.log('Monitor App {0}:{1} Started'\
                 .format(server_name, port_number))

        self.log('Setting environment variables to {0}'\
            .format(self.environment))
        self.set_value('server_name', server_name)
        self.set_value('port_number', port_number)
        self.set_value('ip_addr', host_ip)
        self.set_value('version', version)
        self.set_value('redis_host', 'localhost')
        self.set_value('redis_port', '6379')
        self.set_value('redis_db', '0')
        self.log('Stored environment variables')


    def persist_notification(
        self,
        sender=None,
        recipient=None,
        notification=None,
        action=None,
        event_date=None
    ):
        self.__Notification_Service_db.save_notification(
            sender,
            recipient,
            notification,
            action,
            event_date
        )
        self.log(
          'Persisted Notification: {0} for {1}; Note: {2}; Action: {3}; on {4}'\
          .format(
            sender,
            recipient,
            notification,
            action,
            event_date
          )
        )


    def queue_notification(
        self,
        sender=None,
        recipient=None,
        text=None,
        action=None,
        event_date=None
    ):
        __redis = {'host':self.get_value('redis_host'),
                   'port':self.get_value('redis_port'),
                   'db':self.get_value('redis_db')}
        redis_instance = redis.StrictRedis(**__redis)
        return redis_instance.publish(
            'notification_store',
            '{0}<<*>>{1}<<*>>{2}<<*>>{3}<<*>>{4}'.format(
                sender,
                recipient,
                text,
                action,
                event_date
            )
        )


    def get_queue(self):
        __redis = {'host':self.get_value('redis_host'),
                   'port':self.get_value('redis_port'),
                   'db':self.get_value('redis_db')}
        redis_instance = redis.StrictRedis(**__redis)
        redis_pubsub = redis_instance.pubsub()
        redis_pubsub.subscribe('notification_store')
        return redis_pubsub


    def fetch_notifications(
        self,
        recipient=None
    ):
        return self.__Notification_Service_db.get_notifications(recipient)


    def clear_notification(
        self,
        identifier=None
    ):
        return self.__Notification_Service_db.clear_notification(identifier)


global_control = Control()
