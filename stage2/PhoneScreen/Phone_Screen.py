import redis, atexit, os

# Get OS Environment Variables

try:
    server_name = os.environ.get('serverName')
    redis_port = os.environ.get('redis_port')
except KeyError as ke:
    print('An error occurred!')
    print('------------------')
    print('{0}'.format(ke))
except:
    raise

def close_out():
    print('')
    print('Screen display terminated.')
    print('--------------------------')
    print('{0}'.format(close_action))

close_action = 'Closed by '

r = redis.StrictRedis(host=server_name, port=redis_port, db=0)
r_pubsub = r.pubsub()
r_pubsub.subscribe('output_screen')

atexit.register(close_out)

print('')
print('Screen display starting.')
print('------------------------')
print('')

try:
    for message in r_pubsub.listen():
        if type(message['data']) != int:
            print(message['data'].decode('utf-8').rstrip())
except KeyboardInterrupt as ki:
    close_action += 'user'
except redis.exceptions.ConnectionError as rce:
    close_action += 'server; phone has probably been shutdown.'



