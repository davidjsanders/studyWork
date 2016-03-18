import redis, atexit, os, argparse

try:
    parser = argparse.ArgumentParser(
        description='PhoneScreen.py emulates a phone screen by subscribing '+\
                    'to a redis pubsub queue and listening for messages of '+\
                    'a certain type; when those messages are received, the '+\
                    'phone screen prints the message to stdout. Stdout is '+\
                    'useful as the output can be captured to a file '+\
                    '(e.g. PhoneScreen.py arg1 arg2 > file.out) and multiple '+\
                    'phone screens can listen against a single phone, '+\
                    'emulating many people being able to see the screen.'
    )
    parser.add_argument('--server',
                        type=str,
                        help='The name or IP address of the server. Please '+\
                             'note; this is simply the server name '+\
                             '(e.g. bob) and not the FQDN or http://server. '+\
                             'The server name is used to build the URL '+\
                             'for the redis server.',
                        required=True)
    parser.add_argument('--port',
                        type=int,
                        help='The port number (e.g. 16379) used by the redis '+\
                             'server. Please note; this is simply the port '+\
                             '(e.g. 16379). '+\
                             'The port tells the Python redis client which '+\
                             'port to use. ',
                        required=True)
    args = parser.parse_args()
    server_name = args.server
    redis_port = args.port
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

print('Attempting to connect to {0} on port {1}'\
    .format(server_name, redis_port))

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



