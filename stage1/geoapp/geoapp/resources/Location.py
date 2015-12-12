from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from geoapp import app, api

import geoapp.resources.Config as Config
from geoapp.resources.Response import Response_Object

class Location(Resource):
    def get(self):
        return Response_Object(
                data={'location-x':50, 'location-y':50},
                status=200,
                success_fail='success',
                message='Test Message'
            ).response()

    def post(self):
        return Response_Object(
                data={'test':'SET (put) Location (x,y)'},
                status=200,
                success_fail='success',
                message='Test Message'
            ).response()


