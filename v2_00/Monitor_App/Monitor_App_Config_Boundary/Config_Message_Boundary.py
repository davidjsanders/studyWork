from flask_restful import Resource, reqparse
from Monitor_App_Config_Control.Config_Message_Control \
    import logger_message_object

class Config_Message_Boundary(Resource):
    def get(self, msg=None):
        return_state = logger_message_object.get_message(msg)
        return return_state


    def put(self, msg=None):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = logger_message_object.set_message(msg,\
                                                         json_string=raw_data)

        return return_state


    def delete(self, msg=None):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = logger_message_object.remove_message(msg,\
                                                           json_string=raw_data)

        return return_state


#    def post(self, msg=None):
#        raw_data = None
#        raw_data = reqparse.request.get_data().decode('utf-8')
#        return_state = logger_control_object.set_logger(json_string=raw_data)
#
#        return return_state
#
#
#    def delete(self, msg=None):
#        raw_data = None
#        raw_data = reqparse.request.get_data().decode('utf-8')
#        return_state = logger_control_object.remove_logger(json_string=raw_data)
#
#        return return_state
#
