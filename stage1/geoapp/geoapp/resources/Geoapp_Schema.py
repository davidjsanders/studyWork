from flask_restful import Resource
from geoapp import app, api

from geoapp.resources.Response import Response_Object
import geoapp.resources.Config as Config

class Geoapp_Schema(Resource):
    def get(self):
        schema = {
                    "$schema": "http://json-schema.org/draft-04/schema#",
                    "id": 'http://'+Config.server_name+':'+ \
                          str(Config.port_number)+\
                          api.url_for(Geoapp_Schema,
                                      _external=Config.ext_mode),
                    "type": "object",
                    "properties": {
                        "location":
                        {
                            "type": "string",
                            "description":"The message text to be broadcast",
                            "default":"new note"
                        },
                        "start-x":
                        {
                            "type": "number",
                            "description":"The id (free-form) of the device "+\
                                          "that sent the message.",
                            "default":"0"
                        },
                        "start-y":
                        {
                            "type": "number",
                            "description":"The id (free-form) of the device "+\
                                          "that sent the message.",
                            "default":"0"
                        },
                        "end-x":
                        {
                            "type": "number",
                            "description":"The id (free-form) of the device "+\
                                          "that sent the message.",
                            "default":"0"
                        },
                        "end-y":
                        {
                            "type": "number",
                            "description":"The id (free-form) of the device "+\
                                          "that sent the message.",
                            "default":"0"
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


