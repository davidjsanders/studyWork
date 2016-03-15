from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service.Notification_Service_Database \
    import Notification_Service_Database

import datetime, time, json, redis, os, requests
from textwrap import wrap

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(object):
    __log_file = None
    __Notification_Service_db = None
    __redis = {'host':'localhost', 'port':6379, 'db':0}

    def __init__(self):
        # Get hostname and port from OS. If the environment variables have not
        # been set, e.g. the app is being run locally, then catch an exception
        # and default to Flask's built-in server, localhost on port 5000.
        #
        stage = 0      # A stage indicator to know which variable caused the
                       # exception
        try:
            stage += 1
            port_number = os.environ['portToUse']
            stage += 1
            server_name = os.environ['serverName']
            stage += 1
            host_ip = os.environ['hostIP']
            stage += 1
            version = os.environ['version']
        except KeyError as ke:
            if stage == 1:
                port_number = 5000
                server_name = 'localhost'
            elif stage == 2:
                server_name = 'localhost'
            elif stage == 3:
                host_ip = '127.0.0.1'
            else:
                version = 'v1_00'

        self.__server_name = server_name
        self.__port_number = port_number

        self.__Notification_Service_db = Notification_Service_Database()
        self.__log_file = 'datavolume/'+server_name+'-'+str(port_number)+\
            '-log.txt'

        self.log('Notification Service {0}:{1} Started'\
                 .format(server_name, port_number))

        self.log('Setting server_name to {0}'.format(server_name))
        self.__Notification_Service_db.set_value('server_name', server_name)

        self.log('Setting port number to {0}'.format(port_number))
        self.__Notification_Service_db.set_value('port_number', port_number)

        self.log('Setting Host IP Address to {0}'.format(host_ip))
        self.__Notification_Service_db.set_value('ip_addr', host_ip)

        self.log('Setting version to {0}'.format(version))
        self.__Notification_Service_db.set_value('version', version)
        #self.__redis['host'] = server_name
        #self.__redis['port'] = 6379

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
        redis_instance = redis.StrictRedis(**self.__redis)
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
        redis_instance = redis.StrictRedis(**self.__redis)
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


    def set_value(self, key=None, value=None):
        return self.__Notification_Service_db.set_value(key, value)


    def get_value(self, key=None):
        return self.__Notification_Service_db.get_value(key)


    def clear_value(self, key=None):
        return self.__Notification_Service_db.clear_value(key)


    def db_logger(self,
                  central_logger=None,
                  sender=None,
                  log_type=None,
                  log_message=None
    ):
        if central_logger == None:
            return
        try:
            sender = 'notify_svc_' + str(self.__port_number)
            payload_data = {
                "sender":sender,
                "log-type":"normal",
                "message":log_message
            }
            requests.post(
                central_logger,
                data=json.dumps(payload_data),
                timeout=10 # If nothing after 10s. ignore central
            ) # Ignore return from central logger
        except Exception as e:
            self.log('Notification Service Exception: {0}'\
                         .format(repr(e)),
                     log_to_central=False
                    )


    def log(self,
            log_message=None,
            log_to_central=True
    ):
        now = datetime.datetime.now()
        f = None
        try:
            central_logger = self.get_value('logger')
            if central_logger not in ('', [], None) \
            and log_to_central \
            and log_message != None:
                sender = 'notify_svc_' + str(self.__port_number)
                self.db_logger(central_logger, sender, 'normal', log_message)
            f = open(self.__log_file, 'a')
            if log_message == None or log_message == '':
                f.write("{0:>28s}\n".format(str(now)+': '))
            else:
                wrapped80 = wrap(log_message, 79)
                time_line = [str(now)]
                for line in wrapped80:
                    time_line.append('')
                for i, line in enumerate(wrapped80):
                    f.write('{0:>28s}{1}'.format(time_line[i]+': ', line)+"\n")
        except Exception:
            raise
        finally:
            if not f == None:
                f.close()

    def do_response(self,
                    status=200,
                    response='success',
                    data=None,
                    message=''):
        return_dict = {"status":status,
                       "response":response,
                       "data":data,
                       "message":message}
        return Response(
            json.dumps(return_dict),
            status=status,
            mimetype='application/json')


    def write_console(self, message=None):
        if message == None:
            return

        print(message)

global_control = Control()
