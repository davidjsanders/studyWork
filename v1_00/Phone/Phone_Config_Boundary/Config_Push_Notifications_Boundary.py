from flask_restful import Resource, reqparse
from Phone_Config_Control.Config_Push_Notifications_Control \
    import push_control_object

class Config_Push_Notifications_Boundary(Resource):
    def post(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = push_control_object.request_push(json_string=raw_data)

        return return_state

