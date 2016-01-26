from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Phone import app, api, control, notification_control_object
from Phone_Boundary import apiR
import json

class Notification_Boundary(Resource):
    def post(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        if raw_data == None or raw_data == '':
            return

        json_data = json.loads(raw_data)
        if not 'message' in json_data\
        or not 'key' in json_data\
        or not 'sender' in json_data\
        or not 'action' in json_data:
            return control.do_response(
                    status='400',
                    response='error',
                    data = None,
                    message = 'Badly formed request.'
                )
        else:
            return_state = notification_control_object.incoming_notification(
                text = json_data['message'],
                key = json_data['key'],
                sender = json_data['sender'],
                action = json_data['action']
            )

            return return_state

