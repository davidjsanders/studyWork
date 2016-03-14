from flask_restful import Resource
from flask import Response
from Phone import Control
import json, requests

class Config_Launch_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_controller


    def launch(self, app=None, json_string=None):
        success = 'success'
        status = '200'
        message = 'Phone Monitor App launch status.'
        data = None

        try:
            if json_string == None\
            or json_string == ''\
            or app == None\
            or app == '':
                raise KeyError('Badly formed request. There was no JSON!')

            json_data = json.loads(json_string)
            key = json_data['key']

            if not key == '1234-5678-9012-3456':
                raise ValueError('Control key incorrect.')

            monitor_app = self.__controller.get_value('monitor_app')
            if monitor_app == [] or monitor_app == None:
                data = {'app':app, 'state':'launched'}
            else:
                return_status = self.__notify_monitor(app, monitor_app)
                if 'error' in return_status:
                    status_code = return_status['status']
                    if  status_code == 500:
                        raise requests.exceptions.ConnectionError()
                    elif status_code == 400:
                        raise KeyError()
                    elif status_code == 400:
                        raise ValueError(return_status['message'])
                    else:
                        raise Exception(return_status['message'])
                else:
                    data = return_status
        except requests.exceptions.ConnectionError as rce:
            return {'success':'error',
                    'status':500,
                    'message':'Phone cannot communicate with the monitor '+\
                      'app running at {0}'.format(monitor_app)+\
                      '; the response from the monitor app was'+\
                      ' a connection error: {0}'.format(str(rce))+'.'
                   }
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Key Error: {0}'.format(str(ke))
        except ValueError as ve:
            success = 'error'
            status = '403'
            message = 'Value Error: {0}'.format(str(ve))
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Exception: {0}'.format(str(ve))

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
            if status_code not in (200,201,404):
                raise ValueError('Unable to communicate with monitor app! '+\
                                 'Response code '+\
                                 '{0}'.format(request_response.status_code)+\
                                 ' with data payload '+\
                                 '{0}.'.format(request_response.text)
                                )
            else:
                if status_code == 404\
                and not ('not being monitored' in str(request_response.text)):
                    raise ValueError('Unable to communicate with monitor app.'+\
                                     ' Response from request was {0} {1}.'\
                                     .format(status_code, request_response.text)
                                    )
                json_response = request_response.json()
                if 'error' in json_response:
                    raise ValueError(json_response['message'])
                return {'app':app, 'state':'launched'}
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
            return {'success':'error',
                    'status':500,
                    'message':repr(e)
                   }

launch_control_object = Config_Launch_Control()


