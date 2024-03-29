from flask_restful import Resource
from flask import Response
from Phone import Control
import json, requests

class v3_00_Config_Pair_Control(object):
    controller = None

    def __init__(self):
        self.controller = Control.global_controller


    def is_paired(self):
        success = 'success'
        status = '200'
        message = 'Phone Bluetooth pairing status.'
        data = None

        self.controller.log('Request to get Bluetooth pairing status.',
                              screen=False)
        device_paired = self.controller.get_bluetooth()
        if device_paired == []:
            device_paired = None

        pair_data = {'device':device_paired}

        self.controller.log('Bluetooth pairing status: {0}'.format(pair_data),
                              screen=False)

        return self.controller.do_response(
            message=message,
            data=pair_data,
            status=status,
            response=success
        )


    def remove_pair(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Phone Bluetooth un-pairing request.'
        data = None

        try:
            self.controller.log('Request to un-pair Bluetooth',
                                  screen=False)

            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']

            if not key == '1234-5678-9012-3456':
                raise KeyError('Pairing key incorrect.')

            self.controller.log('Getting phone friendly name',
                                  screen=False)
            phone_name = self.controller.get_value('phonename')

            self.controller.log('Getting current pairing status',
                                  screen=False)
            device_paired = self.controller.get_bluetooth()

            if device_paired in (None,'',[]):
                raise ValueError('The phone is not paired, '+\
                                 'so cannot be un-paired')

            self.controller.log('Communicating with Bluetooth device {0}'\
                                      .format(device_paired),
                                  screen=False)
            bluetooth_url = device_paired + '/pair/' + phone_name
            self.controller.clear_value(device_paired)
            device_paired = self.controller.set_bluetooth(None)
            data = {'device':None}

            request_response = requests.delete(bluetooth_url)
            status_code = request_response.status_code

            if status_code not in (200,201):
                if status_code == 404:
                    raise ValueError('Unable to remove pairing as the '+\
                                     'URL cannot be located.')

                raise ValueError('Unable to remove pairing with device! '+\
                                 'Response code '+\
                                 '{0}'\
                                   .format(request_response.status_code)+\
                                 ' with data payload '+\
                                 '{0}'.format(request_response.text)
                                )

        except requests.exceptions.ConnectionError as rce:
            success = 'warning'
            status = '200'
            message = 'Phone un-paired from {0}'.format(device_paired)+\
                      '; however, the response from the Bluetooth device was'+\
                      ' a connection error: {0}'.format(str(rce))+'. '+\
                      'The Bluetooth device may be unavailable and '+\
                      'so un-pairing could not be confirmed.'
            self.controller.log(message,
                                  screen=False)
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Bluetooth un-pairing key error: {0}'.format(str(ke))
            self.controller.log(message, screen=False)
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = 'Bluetooth un-pairing error: {0}'.format(str(ve))
            self.controller.log(message, screen=False)
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Bluetooth un-pairing exception: {0}'.format(str(ve))
            self.controller.log(message, screen=False)

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def set_pair(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Phone Bluetooth pairing request.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            bluetooth = json_data['bluetooth']
            phone_name = self.controller.get_value('phonename')

            if not key == '1234-5678-9012-3456':
                raise ValueError('Pairing key incorrect.')

            bluetooth_url = bluetooth + '/pair/' + phone_name
            request_response = requests.post(bluetooth_url)
            status_code = request_response.status_code
            if status_code not in (200,201):
                if status_code == 404:
                    raise ValueError('Unable to pair with device as the URL '+\
                                     'cannot be located.')

                raise ValueError('Unable to pair with device! '+\
                                 'Response code '+\
                                 '{0}'.format(request_response.status_code)+\
                                 ' with data payload '+\
                                 '{0}'.format(request_response.text)
                                )
            else:
                bluetooth_key = request_response.json()['data']['key']
                self.controller.set_value(bluetooth, bluetooth_key)
            device_paired = self.controller.set_bluetooth(bluetooth)
            data = {'device':device_paired}
        except requests.exceptions.ConnectionError as rce:
            success = 'error'
            status = '500'
            message = 'Phone cannot be paired with {0}'.format(bluetooth)+\
                      '; the response from the Bluetooth device was'+\
                      ' a connection error: {0}'.format(str(rce))+'. '+\
                      'The Bluetooth device may be unavailable or the URL '+\
                      'may be incorrect.'
            self.controller.log(message, screen=False)
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Bluetooth un-pairing key error: {0}'.format(str(ke))
            self.controller.log(message, screen=False)
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = 'Bluetooth un-pairing key error: {0}'.format(str(ve))
            self.controller.log(message, screen=False)
        except Exception as e:
            success = 'error'
            status = '500'
            message = 'Bluetooth un-pairing exception: {0}'.format(repr(e))
            self.controller.log(message, screen=False)

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

