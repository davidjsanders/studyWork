from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from bluetooth import app, api

import bluetooth.resources.Config as Config
from bluetooth.resources.Response import Response_Object

from jsonschema import validate, exceptions
import json
import sqlite3
import datetime

class Bluetooth_Schema(Resource):
    def get(self):
        return_list = []
        return_status = 200
        return_success_fail = 'success'
        return_message = 'notification schema'
        try:
            f = open(Config.schema_filename,'r')
            schema = json.load(f)
            f.close()
            return_list = schema
        except Exception as e:
            return_status = 400
            return_success_fail = 'error'
            return_message = repr(e)

        return Response_Object(
                data=return_list,
                status=return_status,
                success_fail=return_success_fail,
                message=return_message
            ).response()

class Bluetooth_Helper(Resource):
    def get(self):
#        port_number = "5000"
        ext_mode = False
        links = {'_links':{}}

        return_list = []
        return_status = 200
        return_success_fail = 'success'
        return_message = 'notification schema'

        with app.test_request_context():
            links['_links']['self'] = {
                'identifier':0,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Bluetooth_Helper, _external=ext_mode),
                'rel':'links',
                'description':'Display routes supported by this service.',
                'methods':['GET','OPTIONS','HEAD']}

            links['_links']['schema'] = {
                'identifier':1,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Bluetooth_Schema, _external=ext_mode),
                'rel':'schema',
                'description':'Get the schema for broadcasting messages',
                'methods':['GET','OPTIONS','HEAD']}

            links['_links']['bluetooth'] = {
                'identifier':2,
                'href':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Bluetooth_Helper, _external=ext_mode)+\
                    'bluetooth',
                'schema':'http://'+Config.server_name+':'+str(Config.port_number)+\
                    api.url_for(Bluetooth_Schema, _external=ext_mode),
                'rel':'collection',
                'description':'Display and manipulate the notification list '+\
                    'and post new bluetooth.',
                'methods':['POST','OPTIONS','HEAD']}

        return Response_Object(
                data=links,
                status=return_status,
                success_fail=return_success_fail,
                message=return_message
            ).response()

class Say_Aloud(Resource):
    def post(self, controlkey=None):
        return_list = []
        return_status = 200
        return_success_fail = 'success'
        return_message = 'Message broadcasted via Bluetooth'

        textToSay = None
        try:
            result = Bluetooth_Schema().get().data.decode('utf-8')
            schema = json.loads(result)
            now = datetime.datetime.now()

            # Define f as None so we know if the file opened in exception.
            f = None 

            f = open('datavol/bluetooth_output_'+\
                    str(Config.port_number)+'.txt','a')
            textToSay = json.loads(reqparse.request.get_data().decode('utf-8'))
            validate(textToSay, schema['success']['data'])
            f.write('Device'+str(Config.port_number)+':'+str(now)+\
                    ': '+textToSay['message']+'\n')
            f.close()
        except Exception as e:
            return_status = 400
            return_success_fail = 'error'
            return_message = repr(e)
        finally:
            if not f == None:
                f.close()

        return Response_Object(
                data=textToSay,
                status=return_status,
                success_fail=return_success_fail,
                message=return_message
            ).response()

api.add_resource(Say_Aloud,
                 '/v1_00/bluetooth')
api.add_resource(Bluetooth_Schema,
                 '/v1_00/bluetooth/schema')
api.add_resource(Bluetooth_Helper,
                 '/v1_00/')
