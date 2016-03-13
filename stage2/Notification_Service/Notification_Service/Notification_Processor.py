import redis, requests, json, copy
import time

def redis_close(thread=None, controller=None):
    # Although not used in this app, the thread close event logic would allow
    # us to do any last tasks.
    if not thread == None\
    and not controller == None:
        controller.log('Closing background thread.')
    else:
        controller.log('Thread was none!')

def redis_processor(control_object=None):
    redis_pubsub = control_object.get_queue()

    for message in redis_pubsub.listen():
        if message['type'].upper() == 'MESSAGE':
            control_object.log('Redis Processor: Start. '+\
                               'Message received! {0}'\
                                   .format(message['data']))
            message_data = message['data']
            message_fields = message['data'].decode('utf-8').split('<<*>>', 5)

            try:
                persist_notification = True
                persist_reason = 'unknown'
                time.sleep(2) # Let any caller finish what it was doing first, 
                              # e.g. deleting from the database.
                control_object.log('Redis Processor: '+\
                                   'Message parsed to: {0}'\
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

                temp_payload_data = copy.deepcopy(payload_data)
                temp_payload_data['key']='OBFUSCATED'

                control_object.log('Redis Processor: Payload {0}'\
                  .format(temp_payload_data))

                control_object.log('Redis Processor: issuing http '+\
                                   'request to {0}'\
                  .format(recipient))
                request_response = requests.post(
                    recipient,
                    data=json.dumps(payload_data),
                    timeout=30
                )
                control_object.log('Redis Processor: http request '+\
                                   'response {0}'\
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

                    persist_reason = error_text
                    control_object.log('Redis Processor: Stop ERROR')
                    control_object.log(error_text)
                else:
                    persist_notification = False
                    control_object.log('Redis Processor: dispatched to {0}'\
                      .format(recipient))
                    control_object.log('Redis Processor: Stop SUCCESS')
                    control_object.log()
            except requests.exceptions.ConnectionError as rce:
                persist_reason = str(rce)
                control_object.log('Redis Processor: Stop WARNING')
            except KeyError as ke:
                persist_reason = str(ke)
                control_object.log('Redis: *** STOP ERROR: {0}'.format(str(ke)))
            except Exception as e:
                persist_reason = repr(e)
                control_object.log('Redis: *** STOP ERROR: {0}'.format(repr(e)))

            if persist_notification:
                control_object.log('Redis Processor: Persisting '+\
                                   'notification because {0}'\
                                   .format(persist_reason))
                control_object.persist_notification(
                    sender,
                    recipient,
                    text,
                    action,
                    event_date
                )

