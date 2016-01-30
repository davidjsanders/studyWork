from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App \
    import app, api, control, \
           state_control

from Monitor_App_Boundary import apiR

class State_Boundary(Resource):
    def get(self):
        return state_control.get_state()

class State_Change_Boundary(Resource):
    def post(self, state=None):
        if state.upper() not in ('ON','OFF'):
            return_state = control.do_response(
                response='error',
                status=400,
                data=[],
                message='Supported states are on and off. '+\
                        '{0} is not a supported state.'.format(state)
            )
        else:
            raw_data = None
            raw_data = reqparse.request.get_data().decode('utf-8')
            return_state = state_control.set_state(state, raw_data)

        return return_state

