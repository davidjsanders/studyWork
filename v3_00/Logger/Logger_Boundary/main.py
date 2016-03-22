from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Logger import app, api
from Logger.Control import global_control
from Logger_Boundary.Log_Boundary \
    import Log_Boundary, \
           Log_File_Boundary, \
           Log_Boundary_By_Sender

#
# Get the version of the API
#
version = global_control.get_version()

api.add_resource(Log_Boundary,
                 '/{0}/log'.format(version))
api.add_resource(Log_File_Boundary,
                 '/{0}/logfile'.format(version))
api.add_resource(Log_Boundary_By_Sender,
                 '/{0}/log/<string:sender>'.format(version))

