from flask_restful import Resource, Api, reqparse, abort
from flask import Response
from Logger import app, api

from Logger.Log_Control \
    import global_log_control as log_control

class Log_Boundary(Resource):
    def get(self):
        return log_control.get_log_by_sender()


    def post(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return log_control.update_log(json_string=raw_data)

    def delete(self):
        raw_data = None
        raw_data = reqparse.request.get_data().decode('utf-8')
        return log_control.delete_log(json_string=raw_data)


class Log_Boundary_By_Sender(Resource):
    def get(self, sender=None):
        return log_control.get_log_by_sender(sender)

