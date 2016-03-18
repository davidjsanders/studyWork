import redis
import requests
import json

def redis_close(thread=None, controller=None):
    print()
    print(' * Central logging system shutting down')
    print()
#    if not thread == None\
#    and not controller == None:
#        controller.log('Closing background thread.')
#    else:
#        controller.log('Thread was none!')


def redis_processor(control_object=None):
    __redis = {'host':'localhost', 'port':6379, 'db':0}
    redis_instance = redis.StrictRedis(**__redis)
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

