from flask_restful import Resource
from bluetooth import app, api

from bluetooth.resources.Response import Response_Object
import bluetooth.resources.Config as Config

class Bluetooth_Schema(Resource):
    def get(self):
        schema = {
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "id": 'http://'+Config.server_name+':'+ \
                          str(Config.port_number)+\
                          api.url_for(Bluetooth_Schema,
                                      _external=Config.ext_mode),
                    "type": "object",
                    "properties": {
                        "message":
                        {
                            "type": "string",
                            "description":"The message text to be broadcast",
                            "default":"new note"
                        },
                        "sender":
                        {
                            "type": "string",
                            "description":"The id (free-form) of the device "+\
                                          "that sent the message.",
                            "default":"unknown"
                        },
                        "sensitivity":
                        {
                            "enum" : ["low", "normal", "high", None],
                            "description":"The sensitivity of the message "+\
                                          "(N.B. This is not currently used "+\
                                          "but provided for future use.)",
                            "default":"normal"
                        }
                    },
                 "required": ["message", "sender"]
                 }
        return_list = []
        return_status = 200
        return_success_fail = 'success'
        return_message = 'notification schema'
        try:
            return_list = schema
        except Exception as e:
            return_status = 400
            return_success_fail = 'error'
            return_message = repr(e)

        return Response_Object(
                data=return_list,
                status=return_status,
                success_fail=return_success_fail,
                message=return_message
            ).response()


