from flask_restful import Resource, reqparse
from Phone_Config_Control.Config_Help_Control \
    import help_control_object

class Config_Help_Boundary(Resource):
    def get(self):
        return_state = help_control_object.help()
        return return_state

