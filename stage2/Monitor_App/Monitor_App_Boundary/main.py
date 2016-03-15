from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App import app, api
from Monitor_App.Control import global_control
from Monitor_App_Boundary import apiR
from Monitor_App_Boundary.State_Boundary \
    import State_Boundary, \
           State_Change_Boundary
from Monitor_App_Boundary.App_Launched_Boundary \
    import App_Launched_Boundary
from Monitor_App_Boundary.App_Boundary \
    import App_Boundary, App_All_Boundary

#
# Get the version of the API
#
version = global_control.get_value('version')

apiR.add_resource(State_Boundary, 
                  '/{0}/state'.format(version))
apiR.add_resource(State_Change_Boundary, 
                  '/{0}/state/<string:state>'.format(version))
apiR.add_resource(App_Launched_Boundary, 
                  '/{0}/launched/<string:application>'.format(version))
apiR.add_resource(App_Boundary, 
                  '/{0}/app/<string:application>'.format(version))
apiR.add_resource(App_All_Boundary, 
                  '/{0}/apps'.format(version))

