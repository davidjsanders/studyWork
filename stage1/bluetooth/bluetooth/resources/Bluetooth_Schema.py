from flask_restful import Resource

from bluetooth.resources.Notification import Notification
from bluetooth.resources.Response import Response_Object

class Notification_Schema(Resource):
    def get(self):
        return_list = []
        try:
            return_status = 200
            return_success_fail = 'success'
            return_message = 'notification schema'
            return_list = Notification.__schema__
        except Exception as e:
            return_message = 'An exception occurred: '+repr(e)
            return_success_fail = 'error'
            return_status = 400

        return Response_Object(
            return_list,
            return_status,
            return_success_fail,
            return_message
        ).response()

