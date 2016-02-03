from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth \
    import app, api
from Bluetooth.Control import global_control as control
from Bluetooth.Pairing_Control \
    import global_pair_control as pair_control_object
from Bluetooth.Broadcast_Control \
    import global_broadcast_control as broadcast_control_object
from Bluetooth_Boundary import apiR
import json

class Broadcast_Boundary(Resource):
    def post(self, devicename):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        if raw_data == None or raw_data == '':
            return
        json_data = json.loads(raw_data)
        if not 'message' in json_data\
        or not 'key' in json_data:
            return

        return_state = broadcast_control_object.broadcast_message(
                devicename = devicename,
                text = json_data['message'],
                key = json_data['key']
            )

        return return_state



