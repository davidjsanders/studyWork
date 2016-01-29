from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import app, api, pair_control_object, control
from Bluetooth_Boundary import apiR

class Pair_Boundary(Resource):
    def get(self, devicename):
        return_value = pair_control_object.pair_info(devicename)
        return return_value

    def post(self, devicename):
        return_value = pair_control_object.pair_device(devicename)
        return return_value

    def delete(self, devicename):
        return_value = pair_control_object.pair_unpair(devicename)
        return return_value


