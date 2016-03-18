from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Notification_Service \
    import app, api
from Notification_Service.Notification_Push_Control \
    import global_notification_push_control as notification_push_control
from Notification_Service.Control import global_control as control

class Notification_Push_Boundary(Resource):
    def post(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = notification_push_control\
            .push_notifications(json_string=raw_data)

        return return_state

