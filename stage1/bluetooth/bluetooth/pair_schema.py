from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from bluetooth import app, api

import bluetooth.resources.Config as Config
from bluetooth.resources.Response import Response_Object
from bluetooth.resources.Bluetooth_Schema import Bluetooth_Schema

from jsonschema import validate, exceptions
import json
import datetime

class Pair(Resource):
    def get(self):
        pass


class Pair_Schema(Resource):
    def get(self):
        try:
            schema = {"href":"Blah!"}
            # Return the schema
            return_status = 200
            return_success_fail = 'success'
            return_message = 'notification pair schema'
            return_list = schema
            print(schema)
        except Exception as e:
            return_status = 400
            return_success_fail = 'error'
            return_message = 'An error occurred. '+repr(e)
            return_list = []

        # Return the HTTP response object with data and status. The Response_
        # Object class will create an HTTP Response with the correct data,
        # status code, and mimetype.
        return Response_Object(
            data=return_list,
            status=return_status,
            success_fail=return_success_fail,
            message=return_message
        ).response()

class Bluetooth_Helper(Resource):
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
                    api.url_for(Bluetooth_Helper, _external=Config.ext_mode),
                'rel':'links',
                'description':'Display routes supported by this service.',
                'methods':['GET','OPTIONS','HEAD']}

            links['_links']['schema'] = {
                'identifier':1,
                'href':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Bluetooth_Schema, _external=Config.ext_mode),
                'rel':'schema',
                'description':'Get the schema for broadcasting messages',
                'methods':['GET','OPTIONS','HEAD']}

            links['_links']['bluetooth'] = {
                'identifier':2,
                'href':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Bluetooth_Helper, _external=Config.ext_mode)+\
                    'bluetooth',
                'schema':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Bluetooth_Schema, _external=Config.ext_mode),
                'rel':'collection',
                'description':'Display and manipulate the notification list '+\
                    'and post new bluetooth.',
                'methods':['POST','OPTIONS','HEAD']}

            links['_links']['pair'] = {
                'identifier':3,
                'href':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Bluetooth_Helper, _external=Config.ext_mode)+\
                    'pair',
                'schema':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Pair_Schema, _external=Config.ext_mode),
                'rel':'pair',
                'description':'Invoke device pairing.',
                'methods':['GET','POST','OPTIONS','HEAD']}

            links['_links']['pair-schema'] = {
                'identifier':4,
                'href':'http://'+Config.server_name+':'+ \
                    str(Config.port_number)+\
                    api.url_for(Bluetooth_Helper, _external=Config.ext_mode)+\
                    'pair/schema',
                'rel':'pair-schema',
                'description':'Display the device pairing schema.',
                'methods':['GET','OPTIONS','HEAD']}

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

            output_dict = {
                            "sender":textToSay['sender'],
                            "bluetooth-device":
                                str(Config.server_name)+":"+\
                                str(Config.port_number),
                            "message":textToSay['message'],
                            "date":str(now)
                           }


            validate(textToSay, schema['success']['data'])
            f.write(json.dumps(output_dict)+"\n")
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
api.add_resource(Pair,
                 '/v1_00/pair')
api.add_resource(Pair_Schema,
                 '/v1_00/pair/schema')
api.add_resource(Bluetooth_Helper,
                 '/v1_00/')

