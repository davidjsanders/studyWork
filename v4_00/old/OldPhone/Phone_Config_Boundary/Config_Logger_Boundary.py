from flask_restful import Resource, reqparse
from Phone_Config_Control.Config_Logger_Control \
    import logger_control_object

class Config_Logger_Boundary(Resource):
    def get(self):
        return_state = logger_control_object.get_logger()
        return return_state


    def post(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = logger_control_object.set_logger(json_string=raw_data)

        return return_state


    def delete(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = logger_control_object.remove_logger(json_string=raw_data)

        return return_state

