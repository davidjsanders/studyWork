from flask_restful import Resource, reqparse
from Phone.Location_Control import location_control_object

class Location_Boundary(Resource):
    def get(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = location_control_object.location_request(
                           json_string=raw_data
                       )

        return return_state


