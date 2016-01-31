from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Phone import app, api, control #, pair_control_object
from Phone_Boundary import apiR

class Versions_Boundary(Resource):
    def get(self):
        data = [{
                 "version":1.00,
                 "url":"/v1_00",
                 "description":"First release."}
               ]
        return control.do_response(
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
                            "action":"self",
                            "url":"/v1_00",
                            "rel":"self",
                            "methods":["GET"]
                        }
               }
        return control.do_response(
            message='Versions available list.',
            data=data,
            status=200,
            response='success')

