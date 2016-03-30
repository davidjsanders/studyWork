from flask_restful import Resource, reqparse
from Context_Config_Control.Config_Sample_Control \
    import config_sample_control_object

class Config_Sample_Boundary(Resource):
    def get(self):
        return config_sample_control_object.sample_request()
