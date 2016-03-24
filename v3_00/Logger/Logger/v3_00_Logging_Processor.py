import datetime, time, json, redis, requests

class v3_00_Logging_Processor(object):

    def __init__(self):
        pass

    def redis_close(self, thread=None, controller=None):
        controller.log('{0},{1},{2},{3}'\
            .format(str(datetime.datetime.now()),
                    "logger",
                    "shutdown",
                    "Logging system shutting down.")+"\n")
        print()
        print(' * Central logging system shutting down')
        print()


    def redis_processor(self, control_object=None):
        _redis = {'host':'localhost', 'port':6379, 'db':0}
        redis_instance = redis.StrictRedis(**_redis)
        redis_pubsub = redis_instance.pubsub()
        redis_pubsub.subscribe('central_logger')

        for message in redis_pubsub.listen():
            if message['type'].upper() == 'MESSAGE':
                message_data = message['data']
                message_fields = message['data'].decode('utf-8').split('<<*>>', 5)

                try:
                    sender = message_fields[0]
                    log_type = message_fields[1]
                    text = message_fields[2]
                    timestamp = message_fields[3]

                    control_object.log(sender=sender,
                                       log_type=log_type,
                                       message=text,
                                       timestamp=timestamp)

                except Exception as e:
                    print(repr(e))

