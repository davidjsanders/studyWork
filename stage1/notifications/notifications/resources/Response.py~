from flask import Response
import json

class Response_Object(object):

    def __init__(
        self,
        data,
        status=200,
        success_fail='success',
        message='done',
        mimetype='application/json'
    ):
        self.response_data = data
        self.response_status = status
        self.response_success_fail = success_fail
        self.response_message = message
        self.response_mimetype = mimetype

    def response(self):
        return_dict = {self.response_success_fail:
            {"message":self.response_message,
             "status":self.response_status,
             "data":self.response_data
            }}

        return Response(
            json.dumps(return_dict),
            status=self.response_status,
            mimetype=self.response_mimetype)


