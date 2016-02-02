from flask_restful import Resource
from flask import Response
from Phone import Control
import json, requests

class Config_Monitor_App_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_controller


    def is_launched(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Phone Monitor App launch status.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            monitor_app = self.__controller.get_value('monitor_app')

            if not key == '1234-5678-9012-3456':
                raise ValueError('Control key incorrect.')

            if monitor_app == []:
                monitor_app = None

            data = {'monitor app running at':monitor_app}
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
            #return repr(e)
        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def start(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Phone Monitor App request.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)

            key = json_data['key']
            monitor_app = json_data['monitor-app']
            service = json_data['service']
            recipient = json_data['recipient']

            if not key == '1234-5678-9012-3456':
                raise ValueError('Pairing key incorrect.')

#            server_name = self.__controller.get_value('server_name')
#            port_number = self.__controller.get_value('port_number')

#            recipient = 'http://'+server_name+':'+str(port_number)+'/v1_00'
            monitor_app_url = monitor_app + '/state/on'

            payload = {
                       "key":"1234-5678-9012-3456",
                       "service":service,
                       "recipient":recipient
                      }
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
                state = json_response['data']['state']
                self.__controller.set_value('monitor_app', monitor_app)
                data = {'monitor app':'started at {0}'.format(monitor_app)}
        except requests.exceptions.ConnectionError as rce:
            success = 'error'
            status = '500'
            message = 'Phone cannot communicate with the monitor app running '+\
                      'at {0}'.format(monitor_app)+\
                      '; the response from the monitor app was'+\
                      ' a connection error: {0}'.format(str(rce))+'.'
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = str(ve)
        except Exception as e:
            raise
            #return repr(e)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def stop(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Phone Monitor App request.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)

            key = json_data['key']

            if not key == '1234-5678-9012-3456':
                raise ValueError('Pairing key incorrect.')

            monitor_app = self.__controller.get_value('monitor_app')
            if monitor_app == [] or monitor_app == None:
                raise ValueError('The monitor app is not running.')

            monitor_app_url = monitor_app + '/state/off'

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
                state = json_response['data']['state']
                self.__controller.clear_value('monitor_app')
                data = {'monitor app':'stopped'}
        except requests.exceptions.ConnectionError as rce:
            success = 'error'
            status = '500'
            message = 'Phone cannot communicate with the monitor app running '+\
                      'at {0}'.format(monitor_app)+\
                      '; the response from the monitor app was'+\
                      ' a connection error: {0}'.format(str(rce))+'.'
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = str(ve)
        except Exception as e:
            raise
            #return repr(e)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

monitor_app_control_object = Config_Monitor_App_Control()

