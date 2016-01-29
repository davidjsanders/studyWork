from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service import app, api, control, location_control_object
from Notification_Service_Boundary import apiR

class Location_Boundary(Resource):
    def get(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = location_control_object.location_request(
                           json_string=raw_data
                       )

        return return_state



