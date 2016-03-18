from flask_restful import Resource, reqparse
from Location_Service_Config_Control.Config_Hotspot_Control \
    import config_hotspot_control

class Config_Hotspot_Boundary(Resource):
    def get(self, location):
        return config_hotspot_control.get(location=location)


    def post(self, location):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return config_hotspot_control.set(
            location=location,
            json_string=raw_data)


    def delete(self, location):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return config_hotspot_control.delete(
            location=location,
            json_string=raw_data)

class Config_Hotspot_All_Boundary(Resource):
    def get(self):
        return config_hotspot_control.get_all()

