from flask_restful import Resource
from flask import Response
from Phone import Control
import json, requests

class v3_00_Config_Monitor_App_Control(object):
    controller = None

    def __init__(self):
        self.controller = Control.global_controller


    def is_launched(self):
        success = 'success'
        status = '200'
        message = 'Phone Monitor App launch status.'
        data = None

        try:
            self.controller.log('Request to check Monitor App state.',
                                  screen=False)
            state = 'connected'
            monitor_app = self.controller.get_value('monitor_app')

            if monitor_app == []:
                state = 'disconnected'
                monitor_app = None

            data = {'state':state,
                    'monitor-app':monitor_app}
            self.controller.log('Monitor App state returned as:{0}'\
                                      .format(data),
                                  screen=False)
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Exception: {0}'.format(repr(e))
            self.controller.log(message, screen=False)

        return self.controller.do_response(message=message,
                                             data=data,
                                             status=status,
                                             response=success)


    def start(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Phone Monitor App request.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('No JSON Data!')

            self.controller.log('Request to start Monitor App',
                                  screen=False)

            json_data = json.loads(json_string)

            self.controller.log('Getting JSON data',
                                  screen=False)
            key = json_data['key']
            monitor_app = json_data['monitor-app']
            service = json_data['notification-service']
            location_service = json_data['location-service']

            self.controller.log('Validating key.',
                                  screen=False)
            if not key == '1234-5678-9012-3456':
                raise ValueError('Pairing key incorrect.')

            self.controller.log('Calculating recipient and location provider',
                                  screen=False)

            recipient = 'http://{0}:{1}/{2}/notification'\
                        .format(self.controller.get_value('ip_addr'),
                                self.controller.get_value('port_number'),
                                self.controller.get_value('version'))

            self.controller.log('Set recipient to {0}'.format(recipient),
                                  screen=False)

            location_provider = 'http://{0}:{1}/{2}/location'\
                        .format(self.controller.get_value('ip_addr'),
                                self.controller.get_value('port_number'),
                                self.controller.get_value('version'))

            self.controller.log('Set location provider to {0}'\
                                      .format(location_provider),
                                  screen=False)

            self.controller.log('Setting Monitor App URL',
                                  screen=False)

            monitor_app_url = monitor_app + '/state/on'

            self.controller.log('Monitor App URL set to {0}'\
                                      .format(monitor_app_url),
                                  screen=False)

            payload = {
                       "key":"1234-5678-9012-3456",
                       "notification-service":service,
                       "location-service":location_service,
                       "location-provider":location_provider,
                       "recipient":recipient
                      }

            self.controller.log('Submitting Monitor App start to {0} '\
                                  .format(monitor_app_url)+\
                                  'with payload {0}'.format(payload),
                                  screen=False
                                 )

            request_response = requests.post(monitor_app_url,
                                             json.dumps(payload))

            status_code = request_response.status_code

            self.controller.log('Monitor App request returned status: {0} '\
                                  .format(status_code),
                                  screen=False
                                 )

            if status_code not in (200,201):
                if status_code == 404:
                    raise ValueError('Cannot communicate with monitor app. '+\
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
                self.controller.set_value('monitor_app', monitor_app)
                data = {'state':'connected',
                        'monitor-app':monitor_app}
                self.controller.log('Monitor App returned: {0} '\
                                          .format(data),
                                      screen=False
                                     )
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
            message = 'Start monitor app: {0}'.format(str(ke))
            self.controller.log(message, screen=False)
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = 'Start monitor app: {0}'.format(str(ve))
            self.controller.log(message, screen=False)
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Start monitor app: {0}'.format(repr(e))
            self.controller.log(message, screen=False)

        return_value = self.controller.do_response(message=message,
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
            self.controller.log('Request to sop Monitor App',
                                  screen=False)

            if json_string == None\
            or json_string == '':
                raise KeyError('No JSON data!')

            json_data = json.loads(json_string)

            self.controller.log('Validating key.',
                                  screen=False)

            key = json_data['key']

            if not key == '1234-5678-9012-3456':
                raise ValueError('Pairing key incorrect.')

            self.controller.log('Getting the current Monitor App config.',
                                  screen=False)

            monitor_app = self.controller.get_value('monitor_app')
            if monitor_app == [] or monitor_app == None:
                raise ValueError('The monitor app is not running.')

            self.controller.log('Monitor App currently on {0}'\
                                      .format(monitor_app),
                                  screen=False)

            monitor_app_url = monitor_app + '/state/off'

            payload = {"key":"1234-5678-9012-3456"}

            self.controller.log('Submitting Monitor App stop to {0} '\
                                  .format(monitor_app_url)+\
                                  'with payload {0}'.format(payload),
                                  screen=False
                                 )

            request_response = requests.post(monitor_app_url,
                                             json.dumps(payload))

            status_code = request_response.status_code

            self.controller.log('Monitor App request returned status: {0} '\
                                  .format(status_code),
                                  screen=False
                                 )

            if status_code not in (200,201):
                if status_code == 404:
                    raise ValueError('Cannot communicate with monitor app.'+\
                                     ' Response from request was {0} {1}.'\
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
                self.controller.clear_value('monitor_app')
                data = {'state':'disconnected',
                        'monitor-app':None}
                self.controller.log('Monitor App returned: {0} '\
                                          .format(data),
                                      screen=False
                                     )
        except requests.exceptions.ConnectionError as rce:
            success = 'error'
            status = '500'
            message = 'Phone cannot communicate with the monitor app '+\
                      'at {0}'.format(monitor_app)+\
                      '; the response from the monitor app was'+\
                      ' a connection error: {0}'.format(str(rce))+'.'
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Start monitor app: {0}'.format(str(ke))
            self.controller.log(message, screen=False)
        except ValueError as ve:
            success = 'error'
            status = '400'
            message = 'Start monitor app: {0}'.format(str(ve))
            self.controller.log(message, screen=False)
        except Exception as e:
            success = 'error'
            status = '400'
            message = 'Start monitor app: {0}'.format(repr(e))
            self.controller.log(message, screen=False)

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

