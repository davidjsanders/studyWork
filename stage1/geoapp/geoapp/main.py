from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from geoapp import app, api

import geoapp.resources.Config as Config
from geoapp.resources.Response import Response_Object
from geoapp.resources.Hotspots import Hotspots
from geoapp.resources.Hotspots_Collection import Hotspots_Collection
from geoapp.resources.Hotspots_Schema import Hotspots_Schema
from geoapp.resources.Location import Location
from geoapp.resources.Location_Schema import Location_Schema

from jsonschema import validate, exceptions
import json
import datetime

class Geoapp_Helper(Resource):
    def get(self):
        links = {'_links':{}}

        return_list = []
        return_status = 200
        return_success_fail = 'success'
        return_message = 'notification schema'

        with app.test_request_context():
            links['_links']['self'] = {
                'identifier':0,
                'href':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Geoapp_Helper, _external=Config.ext_mode),
                'rel':'links',
                'description':'Display routes supported by this service.',
                'methods':['GET','OPTIONS','HEAD']}

#            links['_links']['hotspots_schema'] = {
#                'identifier':1,
#                'href':'http://'+Config.server_name+':'+ \
#                    str(Config.port_number)+\
#                    api.url_for(Hotspots_Schema, _external=Config.ext_mode),
#                'rel':'schema',
#                'description':'Get the schema for hotspots',
#                'methods':['GET','OPTIONS','HEAD']}

            links['_links']['hotspots'] = {
                'identifier':1,
                'href':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Geoapp_Helper, _external=Config.ext_mode)+\
                    'hotspots',
                'rel':'collection',
                'description':'Display and manipulate the hotspot list ',
                'methods':['GET','DELETE','OPTIONS','HEAD']}

            links['_links']['hotspots_range'] = {
                'identifier':2,
                'href':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Geoapp_Helper, _external=Config.ext_mode)+\
                    'hotspots?range_from=<int:from>&range_to=<int:to>',
                'rel':'collection',
                'description':'Display and manipulate the hotspot list ',
                'methods':['GET','DELETE','OPTIONS','HEAD']}

            links['_links']['hotspot'] = {
                'identifier':3,
                'href':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Geoapp_Helper, _external=Config.ext_mode)+\
                    'hotspots/<string:hotspot>',
                'schema':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Hotspots_Schema, _external=Config.ext_mode),
                'rel':'item',
                'description':'Display and manipulate a specific hotspot list ',
                'methods':['GET','PUT','POST','DELETE','OPTIONS','HEAD']}

#            links['_links']['location_schema'] = {
#                'identifier':4,
#                'href':'http://'+Config.server_name+':'+ \
#                    str(Config.port_number)+\
#                    api.url_for(Location_Schema, _external=Config.ext_mode),
#                'rel':'schema',
#                'description':'Get the schema for location',
#                'methods':['GET','OPTIONS','HEAD']}

            links['_links']['location'] = {
                'identifier':4,
                'href':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Geoapp_Helper, _external=Config.ext_mode)+\
                    'location',
                'schema':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Location_Schema, _external=Config.ext_mode),
                'rel':'item',
                'description':'Display and set the location',
                'methods':['GET','POST','OPTIONS','HEAD']}

        return Response_Object(
                data=links,
                status=return_status,
                success_fail=return_success_fail,
                message=return_message
            ).response()

#        return Response_Object(
#                data=textToSay,
#                status=return_status,
#                success_fail=return_success_fail,
#                message=return_message
#            ).response()


api.add_resource(Hotspots_Collection,
                 '/v1_00/hotspots')
api.add_resource(Hotspots,
                 '/v1_00/hotspots/<string:hotspot>')
api.add_resource(Hotspots_Schema,
                 '/v1_00/hotspots/schema')
api.add_resource(Location,
                 '/v1_00/location')
api.add_resource(Location_Schema,
                 '/v1_00/location/schema')
api.add_resource(Geoapp_Helper,
                 '/v1_00/')

