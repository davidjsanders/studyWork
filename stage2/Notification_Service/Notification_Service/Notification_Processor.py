import redis
import requests
import json

def redis_close(thread=None, controller=None):
    # Although not used in this app, the thread close event logic would allow
    # us to do any last tasks.
    if not thread == None\
    and not controller == None:
        print('Closing background thread.')
    else:
        print('Thread was none!')

def redis_processor(control_object=None):
    redis_pubsub = control_object.get_queue()

    for message in redis_pubsub.listen():
        if message['type'].upper() == 'MESSAGE':
            message_data = message['data']
            message_fields = message['data'].decode('utf-8').split('<<*>>', 5)

            try:
                control_object.log()
                control_object.log('Redis: *** START HANDLING ***')
                control_object.log('Redis: message received! {0}'\
                  .format(message_fields))
                sender = message_fields[0]
                recipient = message_fields[1]
                text = message_fields[2]
                action = message_fields[3]
                event_date = message_fields[4]

                payload_data = {
                    "key":"NS1234-5678-9012-3456",
                    "message":text,
                    "sender":sender,
                    "action":action
                }
                control_object.log('Redis: Payload {0}'\
                  .format(payload_data))

                control_object.log('Redis: issuing http request to {0}'\
                  .format(recipient+'/notification'))
                request_response = requests.post(
                    recipient+'/notification',
                    data=json.dumps(payload_data),
                    timeout=30
                )
                control_object.log('Redis: http request response {0}'\
                  .format(request_response.status_code))

                if request_response.status_code != 201:
                    error_text = \
                        'Unable to communicate with phone due to error. '
                    if request_response.status_code == 404:
                        error_text += 'The phone (or its URL for '+\
                                      'notifications) could not be found and '+\
                                      'the push returned a not found (404). '+\
                                      'This normally signifies a spelling or '+\
                                      'URL error in the recipient name. '+\
                                      'Message causing error was "'+\
                                      message_data.decode('utf-8')+'"'
                    else:
                        error_text += 'Response status was {0}'\
                                         .format(request_response.status_code)+\
                                      '; '+request_response.json()

                    control_object.log('Redis: *** STOP HANDLING '+\
                        'WITH ERROR ***')
                    print_error(error_text)
                else:
                    control_object.log('Redis: message dispatched to {0}'\
                      .format(recipient))
                    control_object.log('Redis: *** STOP HANDLING '+\
                        'WITH SUCCESS ***')
                    control_object.log()
            except requests.exceptions.ConnectionError as rce:
                print_error(str(rce))
                try:
                    control_object.log('Redis: Persisting notification '+\
                      'because {0}'.format(str(rce)))
                    control_object.log('Redis: *** STOP HANDLING '+\
                        'WITH WARNING - MESSAGE PERSISTED ***')
                    control_object.log()
                    control_object.persist_notification(
                        sender,
                        recipient,
                        text,
                        action,
                        event_date
                    )
                except Exception as e:
                    raise
            except KeyError as ke:
                control_object.log('Redis: *** STOP HANDLING '+\
                    'WITH ERROR ***')
                print_error(str(ke))
            except Exception as e:
                control_object.log('Redis: *** STOP HANDLING '+\
                    'WITH ERROR ***')
                print_error(repr(e))

def print_error(error_message=None):
    print('{0}'.format('-'*80))
    print('*** {0} ***'.format(error_message))
    print('{0}'.format('-'*80))

