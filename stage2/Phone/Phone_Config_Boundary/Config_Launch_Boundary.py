from flask_restful import Resource, reqparse
from Phone import launch_control_object

class Config_Launch_Boundary(Resource):
    def post(self, app):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = launch_control_object.launch(app=app,
                                                    json_string=raw_data)

        return return_state

