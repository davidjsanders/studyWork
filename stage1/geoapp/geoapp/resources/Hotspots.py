from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from geoapp import app, api

import geoapp.resources.Config as Config
from geoapp.resources.Response import Response_Object

class Hotspots(Resource):
    def get(self, hotspot=None):
        return Response_Object(
                data={'hotspot':hotspot if hotspot != None else 'Test',
                      'start-x':0,
                      'start-y':0,
                      'end-x':1000,
                      'end-y':1000
                     },
                status=200,
                success_fail='success',
                message='Test Message'
            ).response()

    def post(self, hotspot=None):
        return Response_Object(
                data={'test':'Add (POST) a new Hotspot'},
                status=200,
                success_fail='success',
                message='Test Message'
            ).response()

    def put(self, hotspot=None):
        return Response_Object(
                data={'test':'Update (PUT) an existing Hotspot'},
                status=200,
                success_fail='success',
                message='Test Message'
            ).response()

    def delete(self, hotspot=None):
        return Response_Object(
                data={'test':'Remove (DELETE) an existing Hotspot'},
                status=200,
                success_fail='success',
                message='Test Message'
            ).response()



