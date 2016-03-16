from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Location_Service import app, api
from Location_Service_Boundary import apiR

from Location_Service.Check_Control \
    import global_check_control as check_control

class Check_Boundary(Resource):
    def get(self):
        return check_control.check()


