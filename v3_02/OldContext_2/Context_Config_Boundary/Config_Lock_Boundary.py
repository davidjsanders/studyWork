from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Phone import app, api
from Phone_Config_Control.Config_Lock_Control import lock_control_object

class Config_Lock_Boundary(Resource):
    def get(self):
        return lock_control_object.is_locked()


    def post(self):
        return lock_control_object.lock_request()


