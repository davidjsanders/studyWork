from flask_restful import Resource, reqparse
from Context.Activity_Control import activity_control_object

class Activities_Boundary(Resource):
    def get(self):
        return activity_control_object.activity_request_all()

class Activity_Boundary(Resource):
    def get(self, activity=None):
        return activity_control_object.activity_request_all()

    def put(self, activity=None):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = activity_control_object.update_activity(
            activity=activity,
            json_string=raw_data
        )

        return return_state




