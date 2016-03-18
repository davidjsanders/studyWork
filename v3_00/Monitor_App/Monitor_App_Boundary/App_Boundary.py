from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Monitor_App.App_Control import global_app_control as app_control
from Monitor_App import app, api

from Monitor_App_Boundary import apiR

class App_Boundary(Resource):
    def get(self, application=None):
        return app_control.get(application)

    def post(self, application=None):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return app_control.set(application, raw_data)

    def delete(self, application=None):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return app_control.delete(application, raw_data)


class App_All_Boundary(Resource):
    def get(self):
        return app_control.get_all()

