from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App import app, api
from Monitor_App_Boundary import apiR
from Monitor_App_Boundary.State_Boundary \
    import State_Boundary, \
           State_Change_Boundary
from Monitor_App_Boundary.App_Launched_Boundary \
    import App_Launched_Boundary
from Monitor_App_Boundary.App_Boundary \
    import App_Boundary, App_All_Boundary

apiR.add_resource(State_Boundary, '/v1_00/state')
apiR.add_resource(State_Change_Boundary,'/v1_00/state/<string:state>')
apiR.add_resource(App_Launched_Boundary,'/v1_00/launched/<string:application>')
apiR.add_resource(App_Boundary,'/v1_00/app/<string:application>')
apiR.add_resource(App_All_Boundary,'/v1_00/apps')

