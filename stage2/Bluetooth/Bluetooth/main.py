from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Bluetooth import app, api
from Bluetooth_Boundary.Versions_Boundary \
    import Versions_Boundary, Version_1_00_Boundary
from Bluetooth_Config_Boundary import main

api.add_resource(Versions_Boundary, '/')
api.add_resource(Version_1_00_Boundary, '/v1_00')
