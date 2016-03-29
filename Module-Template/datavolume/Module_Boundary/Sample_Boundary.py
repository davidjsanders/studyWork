from flask_restful import Resource, reqparse
from Module.Sample_Control import sample_control_object

class Sample_Boundary(Resource):
    def get(self):
        return sample_control_object.sample_request()



