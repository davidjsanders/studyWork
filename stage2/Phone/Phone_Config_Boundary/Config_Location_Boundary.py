from flask_restful import Resource, reqparse
from Phone_Config_Control.Config_Location_Control \
    import config_location_control_object
from Phone.Location_Control import location_control_object

class Config_Location_Boundary(Resource):
    def put(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return_state = config_location_control_object\
                           .set_loc(json_string=raw_data)

        return return_state


    def get(self):
        return location_control_object.location_request()
