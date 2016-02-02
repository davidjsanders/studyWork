from flask_restful import Resource, reqparse
from Phone import pair_control_object

class Config_Pair_Boundary(Resource):
    def get(self):
        return_state = pair_control_object.is_paired()
        return return_state


    def post(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = pair_control_object.set_pair(json_string=raw_data)

        return return_state


    def delete(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = pair_control_object.remove_pair(json_string=raw_data)

        return return_state

