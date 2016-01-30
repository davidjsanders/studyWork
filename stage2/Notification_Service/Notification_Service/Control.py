from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service.Notification_Service_Database \
    import Notification_Service_Database

import datetime, time, json, redis

#
# SuperClass.
# ----------------------------------------------------------------------------
class Control(object):
    __log_file = 'datavolume/Log_File.txt'
    __Notification_Service_db = None
    __redis = {'host':'localhost', 'port':6379, 'db':0}

    def __init__(self):
        self.__Notification_Service_db = Notification_Service_Database()


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
            f.write('{0}: {1}'.format(now,log_message)+"\n")
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

#
# Version 1.00
# ----------------------------------------------------------------------------
class Control_v1_00(Control):
    def future(self):
        pass

