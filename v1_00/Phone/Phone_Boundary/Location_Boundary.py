from flask_restful import Resource, reqparse
from Phone.Location_Control import location_control_object

class Location_Boundary(Resource):
    def get(self):
        return location_control_object.location_request()



