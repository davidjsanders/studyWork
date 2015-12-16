from flask_restful import Resource, Api, reqparse, abort
from notifications import app, api

import notifications.resources.Config as Config
from notifications.resources.Response import Response_Object
from notifications.resources.Notification_Pair_Schema \
    import Notification_Pair_Schema

from jsonschema import validate, exceptions
import json
import requests

class Notification_Lock(Resource):
    def process(self, method='GET'):
        try:
            raw_list=[]
            return_list = []
            return_status = 200
            return_message = 'Device lock status: '
            return_success_fail = 'success'

            if method.upper() == 'GET':
                locked = Config.get_key('locked')

                print(locked)
                if locked.upper() == 'TRUE':
                    return_message += 'locked'
                else:
                    return_message += 'unlocked'
            elif method.upper() == 'POST':
                locked = Config.set_key('locked', 'TRUE')
                return_message += 'locked'
            elif method.upper() == 'PUT':
                locked = Config.set_key('locked', 'FALSE')
                return_message += 'unlocked'
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

    def get(self):
        return self.process()

    def post(self):
        print('Post - 1')
        return self.process(method='POST')

    def put(self):
        __unlock_code = None

        parser = reqparse.RequestParser()
        parser.add_argument('unlock_code', type=int)

        return_range = parser.parse_args()

        __unlock_code = return_range['unlock_code']

        if __unlock_code == None \
        or __unlock_code != 1234:
            print(__unlock_code, return_range)
            return Response_Object(
                [],
                403,
                'error',
                'Invalid lock code provided'
            ).response()

        return self.process(method='PUT')

