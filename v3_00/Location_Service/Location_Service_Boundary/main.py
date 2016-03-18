from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Location_Service.Control import global_control
from Location_Service import app, api
from Location_Service_Boundary import apiR
from Location_Service_Boundary.Check_Boundary import Check_Boundary

#
# Get the version of the API
#
version = global_control.get_value('version')

apiR.add_resource(Check_Boundary, '/{0}/check'.format(version))

