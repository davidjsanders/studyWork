from flask_restful import Resource, reqparse
from Phone_Config_Control.Config_Monitor_App_Control \
    import monitor_app_control_object

class Config_Monitor_App_Boundary(Resource):
    def get(self):
        return monitor_app_control_object.is_launched()


    def post(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = monitor_app_control_object.start(json_string=raw_data)

        return return_state


    def delete(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = monitor_app_control_object.stop(json_string=raw_data)

        return return_state

