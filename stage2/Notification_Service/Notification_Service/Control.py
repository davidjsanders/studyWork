from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service.Notification_Service_Database \
    import Notification_Service_Database

import datetime, time, json, redis, os
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
        except KeyError as ke:
            if stage == 1:
                port_number = 5000
                server_name = 'localhost'
            else:
                server_name = 'localhost'

        self.__server_name = server_name
        self.__port_number = port_number

        self.__Notification_Service_db = Notification_Service_Database()
        self.__log_file = 'datavolume/'+server_name+'-'+str(port_number)+\
            '-log.txt'
        print('Logging to {0}'.format(self.__log_file))

        self.log()
        self.log('*'*78)
        self.log('{0}:{1} Started'.format(server_name, port_number))
        self.log('*'*78)
        self.log()

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
          'Saved Notification: {0} for {1}; Note: {2}; Action: {3}; on {4}'\
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


    def log(self,
            log_message=None
    ):
        now = datetime.datetime.now()
        f = None
        try:
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
