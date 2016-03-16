from flask_restful import Resource, reqparse
from Bluetooth_Config_Control.Config_Output_Control \
    import config_output_control_object

class Config_Output_Boundary(Resource):
    def get(self, devicename):
        return config_output_control_object.get_output(devicename=devicename)


    def post(self, devicename):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return config_output_control_object.set_output(
            devicename=devicename,
            json_string=raw_data)


    def delete(self, devicename):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return config_output_control_object.delete_output(
            devicename=devicename,
            json_string=raw_data)

