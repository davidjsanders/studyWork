from flask_restful import Resource, Api, reqparse, abort
from flask import Response, send_file
from Logger.Control import global_control
import datetime, time, json, requests, redis, sqlite3

#
# SuperClass.
# ----------------------------------------------------------------------------
class v3_00_Log_Control(object):
    controller = None
    redis = {'host':'localhost', 'port':6379, 'db':0}

    def __init__(self):
        self.controller = global_control

    def get_log_file(self):
        success = 'success'
        status = '200'
        message = 'Logging Service, update log.'
        data = None
        try:
            log_file = '{0}'\
                .format(self.controller.get_log_filename())
            print('Fetching {0}'.format(log_file))
            return_response = send_file(log_file)
        except Exception as e:
            error_msg = 'An exception occurred: {0}'.format(repr(e))
            print(error_msg)
            self.controller.log(error_msg, screen=False)

        return return_response


    def get_log_by_sender(self, sender=None):
        success = 'success'
        status = '200'
        message = 'Logging Service, update log.'
        data = None

        retry_limit = 4
        retry_count = 0
        log_returned = []

        while True:
            try:
                success = 'success'
                status = '200'
                message = 'Logging Service, update log.'
                data = None

                log_contents = self.controller.get_log(sender)
                if not log_contents in ([], None, ''):
                    for log in log_contents:
                        log_returned.append(
                          {
                            "sender":log[0],
                            "log-type":log[2],
                            "message":log[3],
                            "timestamp":log[1]
                          }
                        )

                data = {"log":log_returned}
                break
            except sqlite3.OperationalError as soe:
                print('Exception: {0}'.format(str(soe)))
                message = 'Logging service reported unavailable'
                status = 500
                response = 'error'
                retry_count += 1
                if retry_count > retry_limit:
                    print('Exceeded maximum retries. Limit = {0}. Count = {1}'\
                        .format(retry_limit, retry_count))
                    break
                else:
                    print('Retrying operation.')

        return  self.controller.do_response(message=message,
                                              data=data,
                                              status=status,
                                              response=success)


    def delete_log(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Logging Service, clear log.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('No JSON Data passed')

            json_data = json.loads(json_string)

            key = json_data['key']
            if not key == '1234-5678-9012-3456':
                raise ValueError('Logging control key incorrect.')

            self.controller.delete_log()
            data = {'log':[]}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! Missing {0}'.format(str(ke))
            self.controller.log('INTERNAL',
                            'unexpected',
                            message=message,
                            timestamp=str(datetime.datetime.now())
            )
        except ValueError as ve:
            message = str(ve)
            status = 403
            success = 'Error'
            self.controller.log('INTERNAL',
                            'unexpected',
                            message=message,
                            timestamp=str(datetime.datetime.now())
            )
        except Exception as e:
            message = repr(e)
            status = 500
            success = 'error'
            self.controller.log('INTERNAL',
                            'unexpected',
                            message=message,
                            timestamp=str(datetime.datetime.now())
            )

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value




    def update_log(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Logging Service, update log.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)

            try:
                sender = json_data['sender']
                log_type = json_data['log-type']
            except:
                raise

            try:
                text = json_data['message']
                if text in ('', None):
                    raise KeyError('set timestamp')
            except KeyError as ke:
                text = 'No message; timestamp recorded.'

            if sender in (None, '') \
            or log_type in (None, ''):
                raise ValueError(
                  'Value errors: sender and log-type cannot be null'
                )

            now = str(datetime.datetime.now())

            redis_instance = redis.StrictRedis(**self.redis)
            redis_instance.publish(
                'central_logger',
                '{0}<<*>>{1}<<*>>{2}<<*>>{3}'.format(
                    sender,
                    log_type,
                    text,
                    now
              )
            )

            data = {
              "sender":sender,
              "log-type":log_type,
              "message":text,
              "timestamp":now
            }
            print('Logging data: {0}'.format(data))

        except Exception as e:
            success = 'error'
            status = '400'
            message = repr(e)
            self.controller.log(
                'LOGGER',
                'INTERNAL ERROR',
                repr(e),
                str(datetime.datetime.now())
            )

        return  self.controller.do_response(message=message,
                                              data=data,
                                              status=status,
                                              response=success)


