from flask_restful import Resource, reqparse
from Notification_Service.Notification_Receiver \
    import global_notification_receiver_control as notification_receiver_object

class Notification_Receive_Boundary(Resource):
    def post(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = notification_receiver_object\
            .incoming_notification(json_string=raw_data)

        return return_state

