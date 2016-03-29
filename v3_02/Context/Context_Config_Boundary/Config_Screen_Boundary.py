from flask_restful import Resource, reqparse
from Phone_Config_Control.Config_Screen_Control \
    import screen_control_object

class Config_Screen_Boundary(Resource):
    def get(self):
        return_state = screen_control_object.get_screen()
        return return_state

