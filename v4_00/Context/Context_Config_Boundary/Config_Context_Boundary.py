from flask_restful import Resource, reqparse
from Context_Config_Control.Config_Context_Control \
    import context_control_object

class Config_Context_Boundary(Resource):
    def get(self):
        return_state = context_control_object.get_context_engine()
        return return_state


    def put(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = context_control_object\
                           .set_context_engine(json_string=raw_data)
        return return_state


    def delete(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = context_control_object\
                           .clear_context_engine(json_string=raw_data)
        return return_state

