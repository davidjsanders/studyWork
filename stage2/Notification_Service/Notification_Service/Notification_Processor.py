import redis
from pprint import pprint

def redis_processor(control_object=None):
    __redis = {'host':'localhost', 'port':6379, 'db':0}

    # Reference https://pypi.python.org/pypi/redis 

    redis_instance = redis.StrictRedis(**__redis)
    redis_pubsub = redis_instance.pubsub()
    redis_pubsub.subscribe('notification_store')

    for message in redis_pubsub.listen():
        if message['type'].upper() == 'MESSAGE':
            print('Message requires storage and sending')
            message_data = message['data']
            message_fields = message['data'].decode('utf-8').split('<<*>>', 3)
            sender = message_fields[0]
            text = message_fields[1]
            action = message_fields[2]
            event_date = message_fields[3]
            print()
            print('Message:', message_data.decode('utf-8'))
            print()
            print('Sender        :', sender)
            print('Notification  :', text)
            print('Action to take:', action)
            print('Date Issued   :', event_date)
            print()
#            control_object.write_console(message)
#            print(message)

