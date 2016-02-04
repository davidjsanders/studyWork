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
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            service = json_data['service']
            service_url = service + '/push'
            recipient = json_data['recipient']

            if not key == '1234-5678-9012-3456':
                raise ValueError('Control key incorrect.')

            payload = {
                       "key":"1234-5678-9012-3456",
                       "recipient":recipient
                      }
            request_response = requests.post(service_url,
                                             json.dumps(payload))

            status_code = request_response.status_code
            if status_code not in (200,201):
                if status_code == 404:
                    raise ValueError('Unable to communicate with service. '+\
                                     'Response from request was {0} {1}.'\
                                     .format(status_code, request_response.text)
                                    )

                raise ValueError('Unable to communicate with service! '+\
                                 'Response code '+\
                                 '{0}'.format(request_response.status_code)+\
                                 ' with data payload '+\
                                 '{0}.'.format(request_response.text)
                                )
            else:
                json_response = request_response.json()
                if 'error' in json_response:
                    raise ValueError(json_response['message'])
                request_status = json_response['data']['status']
                data = {'notification status':request_status}
        except requests.exceptions.ConnectionError as rce:
            success = 'error'
            status = '500'
            message = 'Phone cannot communicate with notification '+\
                      'service running at {0}'.format(service)+\
                      '; the response from the monitor app was'+\
                      ' a connection error: {0}'.format(str(rce))+'.'+\
                      'The service is probably not running.'
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = str(ve)
        except Exception as e:
            raise

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

