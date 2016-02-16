from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Logger.Control import global_control
import datetime, time, json, requests, redis

#
# SuperClass.
# ----------------------------------------------------------------------------
class Log_Control(object):
    __controller = None
    __redis = {'host':'localhost', 'port':6379, 'db':0}

    def __init__(self):
        self.__controller = global_control

    def get_log_by_sender(self, sender=None):
        success = 'success'
        status = '200'
        message = 'Logging Service, update log.'

        data = {"log":self.__controller.get_log(sender)}

        return  self.__controller.do_response(message=message,
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

            data = {'deleted':self.__controller.delete_log()}
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request! Missing {0}'.format(str(ke))
            self.__controller.log('INTERNAL',
                            'unexpected',
                            message=message,
                            timestamp=str(datetime.datetime.now())
            )
        except ValueError as ve:
            message = str(ve)
            status = 403
            success = 'Error'
            self.__controller.log('INTERNAL',
                            'unexpected',
                            message=message,
                            timestamp=str(datetime.datetime.now())
            )
        except Exception as e:
            message = repr(e)
            status = 500
            success = 'error'
            self.__controller.log('INTERNAL',
                            'unexpected',
                            message=message,
                            timestamp=str(datetime.datetime.now())
            )
            raise

        return_value = self.__controller.do_response(message=message,
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

            sender = json_data['sender']
            log_type = json_data['log-type']
            text = json_data['message']
            now = str(datetime.datetime.now())

            redis_instance = redis.StrictRedis(**self.__redis)
            data = {"Processors receiving":redis_instance.publish(
                'central_logger',
                '{0}<<*>>{1}<<*>>{2}<<*>>{3}'.format(
                    sender,
                    log_type,
                    text,
                    now
                )
              ),
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
            self.__controller.oldlog(
                log_message='Logging service error: {0}'\
                    .format(message))
            raise

        return  self.__controller.do_response(message=message,
                                              data=data,
                                              status=status,
                                              response=success)

global_log_control = Log_Control()
