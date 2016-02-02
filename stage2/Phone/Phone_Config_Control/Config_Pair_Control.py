from flask_restful import Resource
from flask import Response
from Phone import Control
import json, requests

class Config_Pair_Control(object):
    __controller = None

    def __init__(self):
        self.__controller = Control.global_controller


    def is_paired(self):
        success = 'success'
        status = '200'
        message = 'Phone Bluetooth pairing status.'
        data = None

        device_paired = self.__controller.get_bluetooth()
        data = {'paired with':device_paired}
        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def remove_pair(self, json_string=None):
        success = 'success'
        status = '200'
        message = 'Phone Bluetooth un-pairing request.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            phone_name = self.__controller.get_value('phonename')

            if not key == '1234-5678-9012-3456':
                raise ValueError('Pairing key incorrect.')

            device_paired = self.__controller.get_bluetooth()
            if device_paired == None:
                raise ValueError('The phone is not paired, '+\
                                 'so cannot be un-paired')

            bluetooth_url = device_paired + '/pair/' + phone_name
            self.__controller.clear_value(device_paired)
            device_paired = self.__controller.set_bluetooth(None)
            data = {'paired with':None}

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
            phone_name = self.__controller.get_value('phonename')

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
                self.__controller.set_value(bluetooth, bluetooth_key)
            device_paired = self.__controller.set_bluetooth(bluetooth)
            data = {'paired with':device_paired}
        except requests.exceptions.ConnectionError as rce:
            success = 'error'
            status = '500'
            message = 'Phone cannot be paired with {0}'.format(bluetooth)+\
                      '; the response from the Bluetooth device was'+\
                      ' a connection error: {0}'.format(str(rce))+'. '+\
                      'The Bluetooth device may be unavailable and '+\
                      'so un-pairing could not be confirmed.'
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = str(ve)
        except Exception as e:
            raise
            #return repr(e)

        return_value = self.__controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

pair_control_object = Config_Pair_Control()

