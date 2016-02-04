from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App import app, api

from Monitor_App.Control import global_control as control
from Monitor_App.App_Launched_Control \
    import global_app_launched_control as app_launched_control
from Monitor_App_Boundary import apiR

class App_Launched_Boundary(Resource):
    def post(self, application=None):
        if control.get_state().upper() == 'ON':
            raw_data = None
            raw_data = reqparse.request.get_data().decode('utf-8')
            return app_launched_control.app_launched(application, raw_data)
        else:
            message='Monitor App is off and not tracking launches. Unable '+\
                    'to identify if {0} should be monitored!'\
                    .format(application)
            control.log(message)
            return control.do_response(
                    status=400,
                    response='warning',
                    data={"state":"off"},
                    message=message
                   )

