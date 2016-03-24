from flask_restful import Resource
from flask import Response
from Bluetooth.Control \
    import global_control as global_control
from Bluetooth.Pairing_Control \
    import global_pair_control as pair_control_object
import json, requests

class v3_00_Config_Output_Control(object):
    controller = global_control
    pair_controller = pair_control_object

    def __init__(self):
        pass


    def set_output(self, devicename=None, json_string=None):
        success = 'success'
        status = '200'
        message = 'Bluetooth output devices.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            output_item = json_data['output-item']
            file_name = json_data['file-name']

            if not key == '1234-5678-9012-3456':
                raise IndexError('Bluetooth key incorrect.')

            self.controller.log(
                log_message=
                    'Request to add "{0}" to device "{1}" with filename {2}'\
                    .format(output_item, devicename, file_name))

            pairing_key = self.pair_controller.check_pairing(devicename)

            if pairing_key == []:
                raise ValueError('Device {0} is not paired'.format(devicename))
            else:
                state = self.pair_controller\
                    .add_output_device(devicename,
                                       output_item,
                                       'datavolume/'+devicename+'-'+file_name)
                print(state)
                data = {"device":devicename,
                        "output-item":output_item,
                        "file-name":'datavolume/'+devicename+'-'+file_name,
                        "state":"added" if state == True else "not added"}
                self.controller.log(
                    log_message=
                        'Output "{0}" added to device "{1}" (filename: {2})'\
                        .format(output_item, devicename, file_name))
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = str(ke)
            self.controller.log(
                log_message='Output device error: A key is missing: {0}'\
                    .format(message))
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = str(ve)
            self.controller.log(
                log_message='Output device error: {0}'\
                    .format(message))
        except IndexError as ie:
            success = 'error'
            status = '403'
            message = str(ie)
            self.controller.log(
                log_message='Output device error: {0}'\
                    .format(message))
        except Exception as e:
            self.controller.log(
                log_message='Output device error: {0}'\
                    .format(repr(e)))
            raise

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def get_output(self, devicename):
        success = 'success'
        status = '200'
        message = 'Bluetooth output devices.'
        data = None

        try:
            self.controller.log(
                 log_message=
                    'Request to get list of outputs for device "{0}"'\
                    .format(devicename))
            pairing_key = self.pair_controller.check_pairing(devicename)

            if pairing_key == []:
                raise ValueError('Device is not paired')
            else:

                outputs = self.pair_controller.get_output_devices(devicename)
                output_list = []

                for output in outputs:
                    output_list.append({"device":devicename,
                                        "output-item":output[0],
                                        "file-name":output[1],
                                        "state":"ready"
                                       })
                data = {"outputs":output_list}
                self.controller.log(
                    log_message=
                        'Outputs "{0}" setup for device "{1}"'\
                        .format(data['outputs'], devicename))
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = 'Badly formed request!'
            self.controller.log(
                log_message='Output device error: A key is missing: {0}'\
                    .format(message))
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = str(ve)
            self.controller.log(
                log_message='Output device error: {0}'\
                    .format(message))
        except IndexError as ie:
            success = 'error'
            status = '403'
            message = str(ie)
            self.controller.log(
                log_message='Output device error: {0}'\
                    .format(message))
        except Exception as e:
            self.controller.log('Exception: {0}'.format(repr(e)))
            raise

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value


    def delete_output(self, devicename=None, json_string=None):
        success = 'success'
        status = '200'
        message = 'Bluetooth output devices.'
        data = None

        try:
            if json_string == None\
            or json_string == '':
                raise KeyError('Badly formed request!')

            json_data = json.loads(json_string)
            key = json_data['key']
            output_item = json_data['output-item']

            if not key == '1234-5678-9012-3456':
                raise IndexError('Bluetooth key incorrect.')

            self.controller.log(
                 log_message=
                    'Request to remove "{0}" from device "{1}"'\
                    .format(output_item, devicename))

            pairing_key = self.pair_controller.check_pairing(devicename)

            if pairing_key == []:
                raise ValueError('Device {0} is not paired'.format(devicename))
            else:
                state = self.pair_controller\
                    .remove_output_device(devicename, output_item)
                print(state)
                data = {"device":devicename,
                        "output-item":output_item,
                        "file-name":"n/a",
                        "state":"deleted" if state == True else "not deleted"}
                self.controller.log(
                    log_message=
                        'Output "{0}" removed from device "{1}"'\
                        .format(output_item, devicename))
        except KeyError as ke:
            success = 'error'
            status = '400'
            message = str(ke)
            self.controller.log(
                log_message='Output device error: A key is missing: {0}'\
                    .format(message))
        except ValueError as ve:
            success = 'error'
            status = '404'
            message = str(ve)
            self.controller.log(
                log_message='Output device error: {0}'\
                    .format(message))
        except IndexError as ie:
            success = 'error'
            status = '403'
            message = str(ie)
            self.controller.log(
                log_message='Output device error: {0}'\
                    .format(message))
        except Exception as e:
            self.controller.log(
                log_message='Output device error: {0}'\
                    .format(message))
            raise

        return_value = self.controller.do_response(message=message,
                                                     data=data,
                                                     status=status,
                                                     response=success)

        return return_value

