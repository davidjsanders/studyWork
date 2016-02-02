from flask_restful import Resource, reqparse
from flask import Response
from Phone import app, api, lock_control_object

class Config_Unlock_Boundary(Resource):
    def put(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = lock_control_object.unlock_request(json_string=raw_data)

        return return_state

