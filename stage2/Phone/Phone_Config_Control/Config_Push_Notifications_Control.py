from flask_restful import Resource
from flask import Response
from Phone import Control
import json, requests

class Config_Push_Notifications_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_controller


    def request_push(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Phone requesting push of notifications.'
        data = None

        try:
            self.__controller.log('Request to ask Notification Service to '+\
                                  'push persisted notifications.', screen=False)
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            service = json_data['notification-service']
            service_url = service
            recipient = json_data['recipient']

            if not key == '1234-5678-9012-3456':
                raise ValueError('Control key incorrect.')

            payload = {
                       "key":"1234-5678-9012-3456",
                       "recipient":recipient
                      }

            self.__controller.log('Issuing request to notification service '+\
                                  'with payload: {0} '.format(str(payload)),
                                  screen=False)
            request_response = requests.post(service_url,
                                             json.dumps(payload))

            status_code = request_response.status_code
            if status_code not in (200,201,404):
                raise ValueError('Unable to communicate with service! '+\
                                 'Response code '+\
                                 '{0}'.format(request_response.status_code)+\
                                 ' with data payload '+\
                                 '{0}.'.format(request_response.text)
                                )
            else:
                if (status_code == 404 or status_code == 403)\
                and not ('notification-count' in str(request_response.text)):
                    raise ValueError('Unable to communicate with service. '+\
                                     'Response from request was {0} {1}.'\
                                     .format(status_code, request_response.text)
                                    )
                self.__controller.log('Response received from Notification '+\
                                      'Service', screen=False)
                json_response = request_response.json()
                if 'error' in json_response:
                    raise ValueError(json_response['message'])
                request_status = json_response['status']
                data = {'push':json_response['data']}
                self.__controller.log('Received: {0}'.format(str(data)),
                                      screen=False)
        except requests.exceptions.ConnectionError as rce:
            success = 'error'
            status = '500'
            message = 'Phone cannot communicate with notification '+\
                      'service running at {0}'.format(service)+\
                      '; the response from the monitor app was'+\
                      ' a connection error: {0}'.format(str(rce))+'.'+\
                      'The service is probably not running.'
            self.__controller.log(message, screen=False)
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Push request key error: {0}'.format(str(ke))
            self.__controller.log(message, screen=False)
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = 'Push request value error: {0}'.format(str(ve))
            self.__controller.log(message, screen=False)
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Push request exception: {0}'.format(repr(e))
            self.__controller.log(message, screen=False)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def __notify_monitor(self, app=None, monitor_app=None):
        try:
            monitor_app_url = monitor_app + '/launched/' + app

            payload = {"key":"1234-5678-9012-3456"}
            request_response = requests.post(monitor_app_url,
                                             json.dumps(payload))

            status_code = request_response.status_code
            if status_code not in (200,201):
                if status_code == 404:
                    raise ValueError('Unable to communicate with monitor app. '+\
                                     'Response from request was {0} {1}.'\
                                     .format(status_code, request_response.text)
                                    )

                raise ValueError('Unable to communicate with monitor app! '+\
                                 'Response code '+\
                                 '{0}'.format(request_response.status_code)+\
                                 ' with data payload '+\
                                 '{0}.'.format(request_response.text)
                                )
            else:
                json_response = request_response.json()
                if 'error' in json_response:
                    raise ValueError(json_response['message'])
                return {'launched app':app}
        except requests.exceptions.ConnectionError as rce:
            return {'success':'error',
                    'status':500,
                    'message':'Phone cannot communicate with the monitor '+\
                      'app running at {0}'.format(monitor_app)+\
                      '; the response from the monitor app was'+\
                      ' a connection error: {0}'.format(str(rce))+'.'
                   }
        except KeyError as ke:
            return {'success':'error',
                    'status':400,
                    'message':'Badly formed request!'
                   }
        except ValueError as ve:
            return {'success':'error',
                    'status':403,
                    'message':str(ve)
                   }
        except Exception as e:
            raise
            #return repr(e)

push_control_object = Config_Push_Notifications_Control()


