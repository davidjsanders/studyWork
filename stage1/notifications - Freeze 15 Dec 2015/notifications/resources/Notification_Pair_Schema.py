from flask_restful import Resource

from notifications.resources.Response import Response_Object
import notifications.resources.Config as Config
import json

class Notification_Pair_Schema(Resource):
    def get(self):
        return_list = []
        try:
            f = open(Config.__pair_schema_filename__,'r')
            schema = json.load(f)
            f.close()
            return_status = 200
            return_success_fail = 'success'
            return_message = 'notification pair schema'
            return_list = schema
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

