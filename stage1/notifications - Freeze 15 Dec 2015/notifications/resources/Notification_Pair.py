from flask_restful import Resource, Api, reqparse, abort
from notifications import app, api

import notifications.resources.Config as Config
from notifications.resources.Response import Response_Object
from notifications.resources.Notification_Pair_Schema \
    import Notification_Pair_Schema

from jsonschema import validate, exceptions
import json
import requests

class Notification_Pair(Resource):
    def process(self, controlkey=None, method='GET', pair_url=None):
        try:
            raw_list=[]
            return_list = []
            return_status = 200
            return_message = 'Bluetooth pair'
            return_success_fail = 'success'
            schema_context={}

            if controlkey == None or not controlkey == Config.controlkey_master:
                raise RuntimeError('Control Key does not match.')

            if method.upper() == 'GET':
                return_list = Config.get_key('bluetooth')
                if return_list == None:
                    raise RuntimeError('Bluetooth is not paired.')
                return_message += 'ed to '+return_list
            elif method.upper() == 'DELETE':
                paired_device = Config.get_key('bluetooth')
                if paired_device == None:
                    raise RuntimeError('Bluetooth is not paired.')
                return_list = Config.delete_key('bluetooth')
                return_message += 'ing un-paired from {0}.'\
                                      .format(paired_device)
            elif method.upper() == 'POST':
                return_list = Config.set_key('bluetooth', pair_url)
                return_message += 'ed to '+pair_url
                pass

        except exceptions.ValidationError as ve:
            return_message = ve.message
            return_status = 400
            return_success_fail = 'error'
        except RuntimeError as re:
            return_message = str(re)
            return_status = 400
            return_success_fail = 'error'
        except Exception as e:
            return_message = repr(e)
            return_status = 400
            return_success_fail = 'error'

        return Response_Object(
                return_list,
                return_status,
                return_success_fail,
                return_message
            ).response()

    def get(self, controlkey=None):
        return self.process(controlkey=controlkey, method='GET')

    def delete(self, controlkey=None):
        return self.process(controlkey=controlkey, method='DELETE')

    def post(self, controlkey=None):
        raw_json = reqparse.request.get_data().decode('utf-8')
        json_data = json.loads(raw_json)
        schema = json.loads(
                     Notification_Pair_Schema().get().data.decode('utf-8')
                 )['success']['data']

        validate(json_data, schema)

        bluetooth_url = json_data['href']

        return self.process(
                   controlkey=controlkey,
                   method='POST', 
                   pair_url=bluetooth_url
               )

