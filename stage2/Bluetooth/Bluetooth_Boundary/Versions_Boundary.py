from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import app, api, pair_control_object
from Bluetooth_Boundary import apiR

class Versions_Boundary(Resource):
    def get(self):
        data = [{
                 "version":1.00,
                 "url":"/v1_00",
                 "description":"First release."}
               ]
        return pair_control_object.do_response(
            message='Versions available list.',
            data=data,
            status=200,
            response='success')


class Version_1_00_Boundary(Resource):
    def get(self):
        data = {
                "description":"Version 1.00. First Release.",
                "available":"2015-01-25",
                "links":{
                            "action":"pair",
                            "url":"/v1_00/pair",
                            "rel":"pair device",
                            "methods":["GET","POST","DELETE"]
                        }
               }
        return pair_control_object.do_response(
            message='Versions available list.',
            data=data,
            status=200,
            response='success')

