from flask_restful import Resource, reqparse
from Monitor_App_Config_Control.Config_Message_Control \
    import logger_message_object

class Config_App_Message_Boundary(Resource):
    def get(self):
        return_state = logger_message_object.get_app_message()
        return return_state


    def put(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = logger_message_object\
            .set_app_message(json_string=raw_data)

        return return_state

class Config_Location_Message_Boundary(Resource):
    def get(self):
        return_state = logger_message_object.get_location_message()
        return return_state


    def put(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = logger_message_object\
            .set_location_message(json_string=raw_data)
        return return_state


