from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Logger import app, api
from Logger_Boundary.Log_Boundary \
    import Log_Boundary, \
           Log_Boundary_By_Sender

api.add_resource(Log_Boundary, '/v1_00/log')
api.add_resource(Log_Boundary_By_Sender, '/v1_00/log/<string:sender>')

