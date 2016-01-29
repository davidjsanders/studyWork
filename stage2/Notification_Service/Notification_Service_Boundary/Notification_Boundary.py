from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service import app, api, control, notification_control_object
from Notification_Service_Boundary import apiR

class Notification_Boundary(Resource):
    def post(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = notification_control_object.incoming_notification(
            json_string=raw_data
        )

        return return_state

