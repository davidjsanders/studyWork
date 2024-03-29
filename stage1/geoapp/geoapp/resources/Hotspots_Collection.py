from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from geoapp import app, api

import geoapp.resources.Config as Config
from geoapp.resources.Response import Response_Object

class Hotspots_Collection(Resource):
    def check_range_present(self):
        return_range = {}
        temp_range = {}
        __range_from = None
        __range_to = None

        parser = reqparse.RequestParser()
        parser.add_argument('range_from', type=int)
        parser.add_argument('range_to', type=int)

        return_range = parser.parse_args()
        __range_from = return_range['range_from']
        __range_to = return_range['range_to']

        if __range_from != None\
        and int(__range_from) < 0:
            return_range['error'] = Response_Object(
                data={},
                status=400,
                success_fail='error',
                message='From range cannot be less than zero.'
            ).response()
        elif __range_to != None\
        and int(__range_to) < 0:
            return_range['error'] = Response_Object(
                data={},
                status=400,
                success_fail='error',
                message='To range cannot be less than zero.'
            ).response()
        elif (__range_from != None and __range_to != None)\
        and (int(__range_to) < int(__range_from)):
            return_range['error'] = Response_Object(
                data={},
                status=400,
                success_fail='error',
                message='To range cannot be less than from range.'
            ).response()

        return return_range

    def get(self):
        range_check = self.check_range_present()
        if 'error' in range_check:
            return range_check['error']

        start_x = range_check['range_from']
        start_y = range_check['range_to']

        return Response_Object(
                data=[{'hotspot':'TRUE Hot Site 1',
                      'start-x':0 if start_x == None else start_x,
                      'start-y':0 if start_y == None else start_y,
                      'end-x':1000,
                      'end-y':1000
                     },
                      {'hotspot':'Hot Site 2',
                      'start-x':2400,
                      'start-y':2400,
                      'end-x':10000,
                      'end-y':10000
                     }],
                status=200,
                success_fail='success',
                message='Test Message'
            ).response()

    def delete(self):
        range_check = self.check_range_present()
        return Response_Object(
                data={'test':'Remove (DELETE) an existing Hotspot'},
                status=200,
                success_fail='success',
                message='Test Message'
            ).response()



